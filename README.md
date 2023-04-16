# IrisAI
Just experimenting with ChatGPT as a voice assistant.

## Prerequisites

- Python > 3.6 and < 3.10
- DeepSpeech model files: deepspeech-model.pbmm and deepspeech-scorer.scorer
- OpenAI API key

You can get the model and scorer here:
- Model file (.pbmm): https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm
- Scorer file (.scorer): https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer

## Setup

1. Clone the repository:

```
git clone https://github.com/ly0xr/iris.git
cd iris
```

2. Create a virtual environment and activate it:

### For Linux/macOS:

```
python3 -m venv venv
source venv/bin/activate
```

### For Windows (cmd.exe):

```
python -m venv venv
.\venv\Scripts\activate
```

3. Install the required packages:

`pip install -r requirements.txt`

4. Place the DeepSpeech model files deepspeech-model.pbmm and deepspeech-scorer.scorer in the project directory.

5. Set up the OpenAI API key:

Create a .env file in the project directory and add the following line:

`OPENAI_API_KEY=your-api-key-here`

Replace your-api-key-here with your actual OpenAI API key.

6. Run the voice assistant:

`python irisai.py`

The voice assistant will start listening for your voice commands. To exit, press Ctrl+C.

## Troubleshooting

If you encounter issues with the microphone device index, you can list available input devices using the `list_input_devices()` function in the script. Update the `input_device_index` parameter in the `audio.open()` function accordingly.
