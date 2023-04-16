import discord
from modules.gpt_handler import get_gpt3_response
from modules.config import messages


class DiscordHandler(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        input_text = message.content.strip()

        if input_text:
            if not input_text.startswith('!'):
                messages.append(
                    {"role": "user", "content": f"{message.author.name}: {input_text}"})

                try:
                    gpt3_response = get_gpt3_response(messages)
                except Exception as e:
                    gpt3_response = f"Oops! Iris encountered an error: {str(e)}"

                messages.append(
                    {"role": "assistant", "content": gpt3_response})
                await message.channel.send(gpt3_response)
