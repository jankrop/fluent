import json

import requests
from faster_whisper import WhisperModel
from TTS.api import TTS
import numpy as np
from typing import *

whisper = WhisperModel("small", device="cuda", compute_type="float16")
tts = TTS("tts_models/en/ljspeech/glow-tts", progress_bar=True).to("cuda")

def process_conversation(
    audio: list[float],
    sr: int,
    log: list[dict[str, str]],
) -> dict[str, Any]:
    # return {'audio': audio, 'sr': sr, 'log': log}
    with open('/home/jan/fluent-django/test.txt', 'r') as f:
        audio = json.loads(f.read())
    print('Hello from task!')
    audio = np.array(audio)
    print('Transcribing...')
    segments, info = whisper.transcribe(
        '/home/jan/fluent-django/hello.wav', beam_size=5, language='en'
    )
    prompt = "".join([s.text for s in segments])
    log.append({"role": "user", "content": prompt})
    print(prompt)

    r = requests.post(
        "http://127.0.0.1:11434/api/chat",
        json={"model": "mistral", "stream": False, "messages": log},
    )

    result = r.json()["message"]["content"]
    print(result)

    log.append({"role": "assistant", "content": result})

    audio = tts.tts(text=result)
    audio = [float(x) for x in audio]
    print('Goodbye from task!')
    return {'audio': audio, 'sr': 24000, 'log': log}
