from django.shortcuts import render, HttpResponse

from home.llm.llm_graph import LLMGraph


def inference(request):
    return HttpResponse(LLMGraph().inference("How to avoid diabetes."))


def index(request):
    return render(request, 'index.html')


from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json


@ensure_csrf_cookie
def inference(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_type = data.get('userType')
        message = data.get('message')
        history = data.get('history')

        # Process the message and generate a response
        # This is where you'd call your AI model or processing logic
        response = LLMGraph().inference(message)

        return JsonResponse({'response': response})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
