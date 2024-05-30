import hashlib
import uuid

from loguru import logger
from telethon import Button, TelegramClient, events

from openagent.bot.agent import ask, get_pg_memory
from openagent.bot.followup import (
    gen_followup_question,
    get_followup_question,
    store_followup_question,
)
from openagent.bot.random_question import get_random_questions
from openagent.conf.env import settings
from openagent.db.database import DBSession
from openagent.db.models import BotCurrentSession, BotUserSession


class OpenAgentBot:
    def __init__(self):
        self.client = TelegramClient(
            "", settings.TG_API_ID, settings.TG_API_HASH
        ).start(bot_token=settings.TG_BOT_TOKEN)
        self.db_session = DBSession()

    async def get_response_and_send(self, event, question, session_id, reply_to):
        """
        Get response from OpenAgent and send to user
        """
        lc_events = await ask(question=question, session_id=session_id)
        final_answer = ""
        response_msg = await event.respond("🤔 Thinking...", reply_to=reply_to)

        async for lc_event in lc_events:
            kind = lc_event["event"]
            if kind == "on_chat_model_stream":
                final_answer = await self.handle_stream(
                    final_answer, lc_event, response_msg
                )
            if kind == "on_tool_start":
                await self.handle_tool(lc_event, response_msg)
            if kind == "on_chain_end" and lc_event["name"] == "Agent":
                await self.handle_followup(final_answer, response_msg, session_id)

    async def handle_stream(self, final_answer, lc_event, response_msg):
        content = lc_event["data"]["chunk"].content
        if content:
            new_answer = final_answer + content
            if new_answer.strip() != final_answer.strip():
                final_answer = new_answer
                await response_msg.edit(final_answer)
            else:
                final_answer = new_answer
        return final_answer

    async def handle_tool(self, lc_event, response_msg):
        tool_name = lc_event["name"]
        inputs = lc_event["data"].get("input")
        formatted_inputs = ", ".join(f"{k}='{v}'" for k, v in inputs.items())
        output = f"🔧 Starting tool: {tool_name}({formatted_inputs})"
        await response_msg.edit(output)

    async def handle_followup(self, final_answer, response_msg, session_id):
        memory = get_pg_memory(session_id)
        messages = memory.get_messages()
        history = list(map(lambda x: f"{x.type}: {x.content}", messages))
        questions = gen_followup_question(history)[-4:]
        # Generate inline buttons for follow-up questions
        buttons = []
        for fq in questions:
            key = hashlib.md5(fq.encode()).hexdigest()
            store_followup_question(key, fq)
            buttons.append([Button.inline(f"{fq[:30]}", data=key)])
        await response_msg.edit(final_answer, buttons=buttons)

    async def handle_message(self, event):
        """
        Handle new message events
        """
        message_text = event.message.message
        if message_text.strip().startswith("/"):
            return

        user_id = event.chat.id
        logger.info(f"Received message: {message_text}")
        session_id = self.get_current_session_id(user_id)

        await self.get_response_and_send(
            event, message_text, session_id, reply_to=event.message.id
        )

    def get_current_session_id(self, user_id):
        current_session = (
            self.db_session.query(BotCurrentSession)
            .filter(BotCurrentSession.user_id == user_id)
            .all()
        )
        session_id = None
        if len(current_session) == 0:
            session_id = uuid.uuid4().hex
            self.db_session.add(
                BotCurrentSession(user_id=user_id, session_id=session_id)
            )
            self.db_session.add(BotUserSession(user_id=user_id, session_id=session_id))
            self.db_session.commit()
        else:
            session_id = current_session[0].session_id
        return session_id

    async def new_session(self, event):
        """
        Handle /new_session command
        """
        user_id = event.chat.id
        session_id = uuid.uuid4().hex
        self.db_session.query(BotCurrentSession).filter(
            BotCurrentSession.user_id == user_id
        ).delete()
        self.db_session.add(BotCurrentSession(user_id=user_id, session_id=session_id))
        self.db_session.add(BotUserSession(user_id=user_id, session_id=session_id))
        self.db_session.commit()
        await event.respond("🔄 New session started!")

    async def start(self, event):
        """
        Handle /start command
        """
        selected_questions = get_random_questions()
        buttons = [[Button.inline(q, data=q)] for q in selected_questions]
        await event.respond(
            "👋 Welcome to OpenAgent! Here are some questions"
            " you might be interested in:\n\nPlease click on an "
            "option to select a question.",
            buttons=buttons,
        )

    async def help(self, event):
        """
        Handle /help command
        """
        help_text = (
            "🆘 **Help Menu**\n\n"
            "Here are the commands you can use:\n"
            "/start - Start the bot and get some suggested questions.\n"
            "/new_session - Start a new session.\n"
            "/help - Show this help message.\n\n"
            "Just type your question and I'll do my best to assist you!"
        )
        await event.respond(help_text)

    async def handle_question_selection(self, event):
        """
        Handle button click events
        """
        query_data = event.data.decode("utf-8")
        question = get_followup_question(query_data) or query_data
        msg = await event.respond(f"{question}")
        user_id = event.chat.id
        session_id = self.get_current_session_id(user_id)
        await self.get_response_and_send(event, question, session_id, reply_to=msg.id)

    def run(self):
        """
        Main function to initialize and run the Telegram client
        """
        self.client.add_event_handler(self.handle_message, events.NewMessage)
        self.client.add_event_handler(self.start, events.NewMessage(pattern="/start"))
        self.client.add_event_handler(
            self.new_session, events.NewMessage(pattern="/new_session")
        )
        self.client.add_event_handler(self.help, events.NewMessage(pattern="/help"))

        self.client.add_event_handler(
            self.handle_question_selection, events.CallbackQuery
        )
        self.client.start()
        self.client.run_until_disconnected()


if __name__ == "__main__":
    bot = OpenAgentBot()
    bot.run()


# BotFather edit commands
# start - Start the bot and get some suggested questions.
# new_session - Start a new session.
# help - Show help message.
