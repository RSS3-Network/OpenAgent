import random
import uuid

from loguru import logger
from telethon import Button, TelegramClient, events

from openagent.bot.agent import ask
from openagent.conf.env import settings


class OpenAgentBot:
    def __init__(self):
        self.client = TelegramClient(
            "", settings.TG_API_ID, settings.TG_API_HASH
        ).start(bot_token=settings.TG_BOT_TOKEN)
        self.questions = [
            ("What's the current BTC price?", b"1"),
            ("What's the ETH block height?", b"2"),
            ("Any latest DeFi news?", b"3"),
            ("What's the current gas fees?", b"4"),
            ("Top NFT projects right now?", b"5"),
            ("Any recent blockchain updates?", b"6"),
            ("Current trends in the crypto market?", b"7"),
            ("Best platforms for staking?", b"8"),
            ("Upcoming ICOs?", b"9"),
            ("Top crypto exchanges?", b"10"),
            ("Any news on smart contracts?", b"11"),
            ("Current crypto regulations?", b"12"),
            ("Best crypto wallets?", b"13"),
            ("Latest DAO projects?", b"14"),
            ("Current yield farming rates?", b"15"),
            ("Top metaverse projects?", b"16"),
            ("Latest crypto airdrops?", b"17"),
            ("Top crypto influencers?", b"18"),
            ("Current DEX volumes?", b"19"),
            ("Latest news on crypto security?", b"20"),
        ]

    def get_random_questions(self):
        """
        Randomly select five questions from the list
        """
        return random.sample(self.questions, 5)

    async def get_response_and_send(self, event, question):
        """
        Get response from OpenAgent and send to user
        """
        lc_events = await ask(question=question, session_id=uuid.uuid4().hex)
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

    async def handle_message(self, event):
        """
        Handle new message events
        """
        message_text = event.message.message
        if message_text == "/start":
            return

        logger.info(f"Received message: {message_text}")
        await self.get_response_and_send(event, message_text)

    async def start(self, event):
        """
        Handle /start command
        """
        selected_questions = self.get_random_questions()
        buttons = [[Button.inline(q[0], data=q[1])] for q in selected_questions]
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
        question_dict = {
            question[1].decode("utf-8"): question[0] for question in self.questions
        }
        if query_data in question_dict:
            question = question_dict[query_data]
            await event.respond(f"✅ You selected: {question}")
            await self.get_response_and_send(event, question)
        else:
            await event.respond("❌ Unknown option, please select a valid one.")

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
