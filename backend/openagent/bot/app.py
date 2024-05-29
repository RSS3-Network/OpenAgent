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

    async def get_response_and_send(self, event, question, session_id):
        """
        Get response from OpenAgent and send to user
        """
        lc_events = await ask(question=question, session_id=session_id)
        final_answer = ""
        response_msg = await event.respond("🤔 Thinking...")

        async for lc_event in lc_events:
            kind = lc_event["event"]
            if kind == "on_chat_model_stream":
                content = lc_event["data"]["chunk"].content
                if content:
                    final_answer += content
                    await response_msg.edit(final_answer)
            elif kind == "on_tool_start":
                output = (
                    f"🔧 Starting tool: {lc_event['name']}"
                    f" with inputs: {lc_event['data'].get('input')}"
                )
                await response_msg.edit(output)
            elif kind == "on_chain_end":
                if lc_event["name"] == "Agent":
                    await self.handle_followup(final_answer, response_msg, session_id)

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
            buttons.append([Button.inline(f"{fq[:30]}...", data=key)])
        await response_msg.edit(final_answer, buttons=buttons)

    async def handle_message(self, event):
        """
        Handle new message events
        """
        message_text = event.message.message
        if message_text == "/start":
            return

        user_id = event.chat.id
        logger.info(f"Received message: {message_text}")
        session_id = self.get_current_session_id(user_id)

        await self.get_response_and_send(event, message_text, session_id)

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

    async def handle_question_selection(self, event):
        """
        Handle button click events
        """
        query_data = event.data.decode("utf-8")
        question = get_followup_question(query_data) or query_data
        await event.respond(f"✅ You selected: {question}")
        user_id = event.chat.id
        session_id = self.get_current_session_id(user_id)
        await self.get_response_and_send(event, question, session_id)

    def run(self):
        """
        Main function to initialize and run the Telegram client
        """
        self.client.add_event_handler(self.handle_message, events.NewMessage)
        self.client.add_event_handler(self.start, events.NewMessage(pattern="/start"))
        self.client.add_event_handler(
            self.handle_question_selection, events.CallbackQuery
        )
        self.client.start()
        self.client.run_until_disconnected()


if __name__ == "__main__":
    bot = OpenAgentBot()
    bot.run()
