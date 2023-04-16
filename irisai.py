import os
from dotenv import load_dotenv
import deepspeech
import numpy as np
import pyaudio
import requests
import audioop
import pyttsx3

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

headers = {"Authorization": f"Bearer {api_key}"}

# Load the DeepSpeech model
model_path = os.path.join(os.getcwd(), 'deepspeech-model.pbmm')
scorer_path = os.path.join(os.getcwd(), 'deepspeech-scorer.scorer')
model = deepspeech.Model(model_path)
model.enableExternalScorer(scorer_path)

with open("system_prompt.txt", "r") as file:
    system_prompt = file.read()


messages = [{"role": "system", "content": system_prompt}]


# Set up audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

# Initialize the PyAudio library
audio = pyaudio.PyAudio()


# Use this to find out the input device ID of the microphone you want to use
def list_input_devices():
    info = audio.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    for i in range(0, num_devices):
        if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device ID", i, "-",
                  audio.get_device_info_by_host_api_device_index(0, i).get('name'))


def count_tokens(text):
    return len(text.split())


def get_gpt3_response(messages):
    current_token_count = sum(count_tokens(
        message["content"]) for message in messages)

    if current_token_count >= 4000:
        print("Token limit reached. Popping the second message.")
        messages.pop(1)
        current_token_count = sum(count_tokens(
            message["content"]) for message in messages)

    if current_token_count >= 4000:
        raise ValueError(
            "Token count still too high after removing the second message.")

    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        json=data,
        headers=headers,
    )

    response.raise_for_status()
    response_json = response.json()
    return response_json["choices"][0]["message"]["content"].strip()


def record_audio():
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=4)
    frames = []
    speech_detected = False
    print("Listening...")

    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        rms = audioop.rms(data, 2)  # Compute RMS of the audio data

        is_speech = rms > 100  # Set a threshold to determine if speech is detected

        if is_speech:
            frames.append(data)
            speech_detected = True
        elif speech_detected and not is_speech:
            break

    stream.stop_stream()
    stream.close()
    return b"".join(frames)


def speak(text):
    engine = pyttsx3.init()
    # Set the speech rate; you can change this for faster or slower speech
    engine.setProperty('rate', 200)
    # Set the voice; you can change the index for a different voice
    engine.setProperty('voice', engine.getProperty('voices')[1].id)
    engine.say(text)
    engine.runAndWait()


# Main loop
while True:
    try:
        audio_data = record_audio()
        audio_data_np = np.frombuffer(audio_data, dtype=np.int16)
        text = model.stt(audio_data_np)

        if text.strip():
            messages.append({"role": "user", "content": text})
            gpt3_response = get_gpt3_response(messages)
            messages.append({"role": "assistant", "content": gpt3_response})

            print(f"You: {text}")
            print(f"Iris: {gpt3_response}")
            speak(gpt3_response)

    except KeyboardInterrupt:
        print("Exiting...")
        break
