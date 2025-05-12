from fluent.celery import app
from . import llm

@app.task
def process_conversation(audio, sr, conversation):
    return llm.process_conversation(audio, sr, conversation)

