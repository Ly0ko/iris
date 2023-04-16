import pyaudio
import audioop

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
audio = pyaudio.PyAudio()


def list_input_devices():
    info = audio.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    for i in range(0, num_devices):
        if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device ID", i, "-",
                  audio.get_device_info_by_host_api_device_index(0, i).get('name'))


def record_audio():
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=4)
    frames = []
    speech_detected = False
    print("Listening...")

    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        rms = audioop.rms(data, 2)
        is_speech = rms > 200

        if is_speech:
            frames.append(data)
            speech_detected = speech_detected = True
        elif speech_detected and not is_speech:
            break

    stream.stop_stream()
    stream.close()
    return b"".join(frames)


def speak(text, engine):
    engine.setProperty('rate', 200)
    engine.setProperty('voice', engine.getProperty('voices')[1].id)
    engine.say(text)
    engine.runAndWait()
