import os

model_path = os.path.join(os.getcwd(), 'deepspeech-model.pbmm')
scorer_path = os.path.join(os.getcwd(), 'deepspeech-scorer.scorer')

with open("system_prompt.txt", "r") as file:
    system_prompt = file.read()

messages = [{"role": "system", "content": system_prompt}]
