from django.shortcuts import render, HttpResponse

from home.llm.llm_graph import LLMGraph


# Create your views here.
def home(request):
    return HttpResponse("It works")


def inference(request):
    return HttpResponse( LLMGraph().inference("How to avoid diabetes.") )
