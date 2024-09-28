from django.shortcuts import render
from django.utils import timezone

from home.db_schema.chat_history import ChatHistory
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
        user_timestamp = data.get('timestamp')  # Get timestamp from frontend

        llm_graph = LLMGraph()
        response = llm_graph.inference(message, history)

        # Create user message entry
        user_entry = ChatHistory.objects.create(
            patient_id=1,
            chat_id=1,
            is_user=True,
            text=message,
            timestamp=timezone.datetime.fromtimestamp(user_timestamp / 1000.0, tz=timezone.get_current_timezone())
        )

        # Create AI message entry
        ai_timestamp = timezone.now()
        ai_entry = ChatHistory.objects.create(
            patient_id=1,
            chat_id=1,
            is_user=False,
            text=response,
            timestamp=ai_timestamp
        )

        return JsonResponse({
            'response': response,
            'user_timestamp': user_entry.timestamp.timestamp() * 1000,  # Convert to milliseconds
            'ai_timestamp': ai_timestamp.timestamp() * 1000  # Convert to milliseconds
        })
    else:
        return JsonResponse({'error': 'There was an error in the request to the server.'}, status=405)
