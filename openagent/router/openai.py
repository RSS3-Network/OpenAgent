import time
import uuid
from typing import List, Optional, Dict, Any
import traceback
import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from langchain.schema import HumanMessage
from loguru import logger
from pydantic import BaseModel, Field

from openagent.conf.llm_provider import get_available_providers
from openagent.workflows.workflow import build_workflow

router = APIRouter(tags=["openai"])


class ToolCall(BaseModel):
    id: str = Field(default_factory=lambda: f"call_{str(uuid.uuid4())}")
    type: str = "function"  # OpenAI currently only supports "function"
    function: Dict[str, Any]


class ChatFunctionCall(BaseModel):
    name: str
    arguments: str


class ChatMessage(BaseModel):
    role: str = Field(example="user")
    content: Optional[str] = Field(example="What's the current market situation for Bitcoin?")
    name: Optional[str] = Field(default=None, example=None)
    tool_calls: Optional[List[ToolCall]] = None
    function_call: Optional[ChatFunctionCall] = None


class ChatCompletionRequest(BaseModel):
    model: str = Field(example="gpt-4o-mini")
    messages: List[ChatMessage] = Field(
        example=[
            {
                "role": "user",
                "content": "What's the current market situation for Bitcoin?"
            }
        ]
    )
    temperature: Optional[float] = Field(default=1.0, example=0.7)
    top_p: Optional[float] = Field(default=1.0, example=1.0)
    n: Optional[int] = Field(default=1, example=1)
    stream: Optional[bool] = Field(default=False, example=False)
    stop: Optional[List[str]] = Field(default=None, example=None)
    max_tokens: Optional[int] = Field(default=None, example=None)
    presence_penalty: Optional[float] = Field(default=0, example=0)
    frequency_penalty: Optional[float] = Field(default=0, example=0)
    user: Optional[str] = Field(default=None, example=None)


class ChatChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: str


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-{str(uuid.uuid4())}")
    object: str = "chat.completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[ChatChoice]
    usage: Usage


class DeltaMessage(BaseModel):
    role: Optional[str] = None
    content: Optional[str] = None


class StreamChoice(BaseModel):
    index: int
    delta: DeltaMessage
    finish_reason: Optional[str] = None


class ChatCompletionStreamResponse(BaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-{str(uuid.uuid4())}")
    object: str = "chat.completion.chunk"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[StreamChoice]


@router.post(
    "/v1/chat/completions",
    summary="Create a chat completion",
    description="""Create a model response for the given chat conversation.
    The endpoint first processes the chat through a workflow agent that can utilize various tools
    and capabilities to provide comprehensive responses.""",
    response_model=ChatCompletionResponse,
    responses={
        200: {
            "description": "Successful response",
            "content": {
                "application/json": {
                    "example": {
                        "id": "chatcmpl-123abc",
                        "object": "chat.completion",
                        "created": 1677858242,
                        "model": "gpt-4o-mini",
                        "choices": [
                            {
                                "index": 0,
                                "message": {
                                    "role": "assistant",
                                    "content": "Based on current market analysis, Bitcoin is showing significant momentum..."
                                },
                                "finish_reason": "stop"
                            }
                        ],
                        "usage": {
                            "prompt_tokens": 50,
                            "completion_tokens": 100,
                            "total_tokens": 150
                        }
                    }
                },
                "text/event-stream": {
                    "example": """data: {"id":"chatcmpl-123abc","object":"chat.completion.chunk","created":1677858242,"model":"gpt-4o-mini","choices":[{"index":0,"delta":{"role":"assistant"},"finish_reason":null}]}

data: {"id":"chatcmpl-123abc","object":"chat.completion.chunk","created":1677858242,"model":"gpt-4o-mini","choices":[{"index":0,"delta":{"content":"Based"},"finish_reason":null}]}

data: {"id":"chatcmpl-123abc","object":"chat.completion.chunk","created":1677858242,"model":"gpt-4o-mini","choices":[{"index":0,"delta":{"content":" on"},"finish_reason":null}]}

data: {"id":"chatcmpl-123abc","object":"chat.completion.chunk","created":1677858242,"model":"gpt-4o-mini","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

data: [DONE]"""
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "An error occurred while processing your request"
                    }
                }
            }
        }
    }
)
async def create_chat_completion(request: ChatCompletionRequest):
    try:
        if request.stream:
            return StreamingResponse(
                stream_chat_completion(request),
                media_type='text/event-stream'
            )

        llm = get_available_providers()[request.model]
        agent = build_workflow(llm)

        combined_message = "\n".join([f"{msg.role}: {msg.content}" for msg in request.messages])
        
        tool_calls = []
        assistant_message = None

        async for event in agent.astream_events(
            {"messages": [HumanMessage(content=combined_message)]},
            version="v1"
        ):
            if event["event"] == "on_tool_end":
                tool_name = event["name"]
                tool_output = event["data"]["output"]
                
                tool_call = ToolCall(
                    function={
                        "name": tool_name,
                        "arguments": json.dumps(tool_output)
                    }
                )
                tool_calls.append(tool_call)
            
            elif event["event"] == "on_chat_model_stream":
                if isinstance(event["data"]["chunk"].content, str):
                    assistant_message = (assistant_message or "") + event["data"]["chunk"].content

        if not assistant_message and not tool_calls:
            raise ValueError("No response generated from the agent")

        # Construct OpenAI format response
        choice = ChatChoice(
            index=0,
            message=ChatMessage(
                role="assistant", 
                content=assistant_message,
                tool_calls=tool_calls if tool_calls else None
            ),
            finish_reason="stop"
        )

        # Estimate token usage
        prompt_tokens = sum(len(msg.content.split()) * 1.3 for msg in request.messages)
        completion_tokens = len(assistant_message.split()) * 1.3 if assistant_message else 0
        
        usage = Usage(
            prompt_tokens=int(prompt_tokens),
            completion_tokens=int(completion_tokens),
            total_tokens=int(prompt_tokens + completion_tokens)
        )

        return ChatCompletionResponse(
            model=request.model,
            choices=[choice],
            usage=usage
        )

    except Exception as e:
        error_msg = f"Error in create_chat_completion: {str(e)}\nTraceback:\n{traceback.format_exc()}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )


async def stream_chat_completion(request: ChatCompletionRequest):
    try:
        llm = get_available_providers()[request.model]
        agent = build_workflow(llm)

        # Send role information
        chunk = ChatCompletionStreamResponse(
            model=request.model,
            choices=[StreamChoice(
                index=0,
                delta=DeltaMessage(role="assistant"),
            )]
        )
        yield f"data: {chunk.json()}\n\n"

        combined_message = "\n".join([f"{msg.role}: {msg.content}" for msg in request.messages])

        async for event in agent.astream_events(
                {"messages": [HumanMessage(content=combined_message)]},
                version="v1"
        ):
            if event["event"] == "on_chat_model_stream":
                chunk_content = event["data"]["chunk"].content
                if chunk_content:
                    chunk = ChatCompletionStreamResponse(
                        model=request.model,
                        choices=[StreamChoice(
                            index=0,
                            delta=DeltaMessage(content=chunk_content, role="assistant"),
                        )]
                    )
                    yield f"data: {chunk.json()}\n\n"
            elif event["event"] == "on_tool_end":
                # Handle tool responses
                tool_name = event["name"]
                tool_output = event["data"]["output"]
                
                # Create a tool call response
                tool_call = ToolCall(
                    function={
                        "name": tool_name,
                        "arguments": json.dumps(tool_output)
                    }
                )
                
                chunk = ChatCompletionStreamResponse(
                    model=request.model,
                    choices=[StreamChoice(
                        index=0,
                        delta=DeltaMessage(
                            tool_calls=[tool_call]
                        ),
                    )]
                )
                yield f"data: {chunk.json()}\n\n"

        # Send end markers
        chunk = ChatCompletionStreamResponse(
            model=request.model,
            choices=[StreamChoice(
                index=0,
                delta=DeltaMessage(),
                finish_reason="stop"
            )]
        )
        yield f"data: {chunk.json()}\n\n"
        yield "data: [DONE]\n\n"

    except Exception as e:
        error_msg = f"Error in stream_chat_completion: {str(e)}\nTraceback:\n{traceback.format_exc()}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )
