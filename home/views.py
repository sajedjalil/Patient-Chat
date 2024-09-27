from django.shortcuts import render
from home.llm.llm_graph import LLMGraph
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def inference(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_type = data.get('userType')
        message = data.get('message')
        history = data.get('history', [])

        llm_graph = LLMGraph()
        response = llm_graph.inference(message, history)

        return JsonResponse({'response': response})
    else:
        return JsonResponse({'error': 'There was an error in the request to the server.'}, status=405)
