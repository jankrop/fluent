import time

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import librosa
import numpy as np

from .models import Conversation
from .llm import process_conversation

def index(request):
    if request.user.is_authenticated:
        conversations = request.user.conversation_set.all()
        return render(request, 'index.html', {'conversations': conversations})
    else:
        return redirect('login')

@login_required
def conversation(request, pk):
    conv = get_object_or_404(Conversation, pk=pk)
    return render(request, 'conversation.html', {'conversation': conv})

@login_required
def send_message(request, pk):
    conv = get_object_or_404(Conversation, pk=pk)
    audio_file = request.FILES['audio']
    print(audio_file.size)
    if audio_file.size > 5 * 1024 * 1024:  # 5 MB
        return JsonResponse({'error': 'Audio file too big'}, status=400)
    # audio, sr = librosa.load(audio_file, sr=None)
    print('hello', time.time())
    # task = process_conversation.delay(audio.tolist(), sr, conv.log)
    # llm_output = process_conversation(audio.tolist(), sr, conv.log)
    llm_output = process_conversation(audio_file, conv.log)
    print('hello again', time.time())
    # return JsonResponse({'task_id': task.id})
    conv.log = llm_output['log']
    conv.save()
    return JsonResponse(llm_output)

@login_required
def check_message_status(request, task_id):
    # task_result = AsyncResult(task_id, app=app)
    # response = {
    #     'status': task_result.status,
    #     'result': task_result.result if task_result.state == 'SUCCESS' else None,
    # }
    # return JsonResponse(response)
    return JsonResponse({})
