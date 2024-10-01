from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import uuid

from home.constants.constants import summarize_trigger_count
from home.models.chat_history import ChatHistory
from home.models.patient import Patient
from home.llm.llm_graph import LLMGraph


def index(request):
    return render(request, 'index.html')


@csrf_exempt
@require_http_methods(["POST"])
def inference(request):
    data = json.loads(request.body)
    message = data['message']
    history = data.get('history', [])
    user_timestamp = data.get('timestamp')
    thread_id = data.get('threadId')

    llm_graph = LLMGraph()

    if len(history) >= summarize_trigger_count:
        summary = get_latest_summary(patient_id=1, is_user=False, thread_id=thread_id)

        history = [
            {
                "role": "user",
                "content": "Provide me with the conversation summary"
            },
            {
                "role": "assistant",
                "content": summary
            }
        ]

    response, summary = llm_graph.inference(message, history, thread_id)

    user_entry, ai_entry = save_chat_entries_db(message, response, summary, user_timestamp, thread_id)

    return JsonResponse({
        'response': response,
        'user_timestamp': user_entry.timestamp.timestamp() * 1000,
        'ai_timestamp': ai_entry.timestamp.timestamp() * 1000
    })


def save_chat_entries_db(user_message, ai_response, summary, user_timestamp, thread_id):
    user_entry = ChatHistory.objects.create(
        patient_id=1,
        thread_id=thread_id,
        is_user=True,
        text=user_message,
        timestamp=timezone.datetime.fromtimestamp(user_timestamp / 1000.0, tz=timezone.get_current_timezone())
    )

    ai_entry = ChatHistory.objects.create(
        patient_id=1,
        thread_id=thread_id,
        is_user=False,
        text=ai_response,
        summary=summary,
        timestamp=timezone.now()
    )

    return user_entry, ai_entry


def get_latest_summary(patient_id, is_user, thread_id):
    latest_chat = ChatHistory.objects.filter(
        Q(patient_id=patient_id) &
        Q(is_user=is_user) &
        Q(thread_id=thread_id)
    ).order_by('-timestamp').first()

    return latest_chat.summary if latest_chat else None


class DateTimeEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, timezone.datetime):
            return obj.strftime('%m-%d-%Y %H:%M:%S')
        return super().default(obj)


@csrf_exempt
@require_http_methods(["GET"])
def get_user_info(request):
    patient = Patient.objects.first()
    if not patient:
        return JsonResponse({'error': 'No patient found'}, status=404)

    return JsonResponse({
        'first_name': patient.first_name,
        'last_name': patient.last_name,
        'date_of_birth': patient.date_of_birth,
        'phone_number': patient.phone_number,
        'email': patient.email,
        'medical_conditions': patient.medical_conditions,
        'medication_regimen': patient.medication_regimen,
        'last_appointment': patient.last_appointment,
        'next_appointment': patient.next_appointment,
        'doctor_name': patient.doctor_name,
    }, encoder=DateTimeEncoder)


@csrf_exempt
@require_http_methods(["GET"])
def get_unique_thread_id(request):
    return JsonResponse({
        'thread_id': uuid.uuid4()
    })
