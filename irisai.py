import threading
import subprocess
import os
import discord
import numpy as np
import deepspeech
import pyttsx3
import asyncio
from dotenv import load_dotenv

from modules.audio_handler import record_audio, speak
from modules.gpt_handler import get_gpt3_response
from modules.config import model_path, scorer_path, messages
from modules.discord_handler import DiscordHandler

load_dotenv()

model = deepspeech.Model(model_path)
model.enableExternalScorer(scorer_path)

running = True


def open_folder(path):
    if os.name == 'nt':  # Windows
        os.startfile(path)
    elif os.name == 'posix':  # macOS and Linux
        subprocess.Popen(['open', path])
    else:
        print(f"Unsupported platform: {os.name}")


def run_discord_handler(discord_token):
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    discord_handler = DiscordHandler(intents)

    def start_discord_handler():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(discord_handler.start(discord_token))

    thread = threading.Thread(target=start_discord_handler)
    thread.start()

    return discord_handler


async def main():
    discord_token = os.environ.get("DISCORD_TOKEN")
    engine = pyttsx3.init()

    if discord_token:
        discord_handler = run_discord_handler(discord_token)
    else:
        print("Discord token not found. Skipping Discord handler...")
        discord_handler = None

    while True:
        try:
            audio_data = record_audio()
            audio_data_np = np.frombuffer(audio_data, dtype=np.int16)
            text = model.stt(audio_data_np)

            if text.strip():
                messages.append({"role": "user", "content": f"Ly0ko: {text}"})
                gpt3_response = get_gpt3_response(messages)
                messages.append(
                    {"role": "assistant", "content": gpt3_response})

                print(f"You: {text}")
                print(f"Iris: {gpt3_response}")
                speak(gpt3_response, engine)

        except KeyboardInterrupt:
            print("Exiting...")
            if discord_handler:
                await discord_handler.close()
            break

if __name__ == "__main__":
    asyncio.run(main())
