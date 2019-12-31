from django.shortcuts import render
import json
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from logging import getLogger
logger = getLogger(__name__)

@ensure_csrf_cookie
# Create your views here.
def auth(request):
    if request.method == 'GET':
        return JsonResponse({})

    ret = {
        "data":"param1:",
    }
    return JsonResponse(ret)
