import subprocess
import os
import numpy as np
import deepspeech
import pyttsx3
from dotenv import load_dotenv

from modules.audio_handler import record_audio, speak
from modules.gpt_handler import get_gpt3_response
from modules.config import model_path, scorer_path, messages

load_dotenv()

model = deepspeech.Model(model_path)
model.enableExternalScorer(scorer_path)


# this is being used in WIP code adding NLU component
def open_folder(path):
    if os.name == 'nt':  # Windows
        os.startfile(path)
    elif os.name == 'posix':  # macOS and Linux
        subprocess.Popen(['open', path])
    else:
        print(f"Unsupported platform: {os.name}")


def main():
    engine = pyttsx3.init()

    while True:
        try:
            audio_data = record_audio()
            audio_data_np = np.frombuffer(audio_data, dtype=np.int16)
            text = model.stt(audio_data_np)

            if text.strip():
                messages.append({"role": "user", "content": text})
                gpt3_response = get_gpt3_response(messages)
                messages.append(
                    {"role": "assistant", "content": gpt3_response})

                print(f"You: {text}")
                print(f"Iris: {gpt3_response}")
                speak(gpt3_response, engine)

        except KeyboardInterrupt:
            print("Exiting...")
            break


if __name__ == "__main__":
    main()
