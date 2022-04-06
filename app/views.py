# webpush
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification
from django.conf import settings
import json


@require_POST
# @csrf_exempt  # del metodo original
def send_push(request):

    # # metodo original
    # try:
    #     body = request.body
    #     data = json.loads(body)
    #
    #     if 'head' not in data or 'body' not in data or 'id' not in data:
    #         return JsonResponse(status=400, data={"message": "Invalid data format"})
    #
    #     user_id = data['id']
    #     user = get_object_or_404(User, pk=user_id)
    #     payload = {'head': data['head'], 'body': data['body']}
    #     send_user_notification(user=user, payload=payload, ttl=1000)
    #
    #     return JsonResponse(status=200, data={"message": "Web push successful"})
    # except TypeError:
    #     return JsonResponse(status=500, data={"message": "An error occurred"})

    # con forms
    existe_error = 0
    error = ""

    try:
        if not 'head' in request.POST.keys() or not 'body' in request.POST.keys() or not 'id' in request.POST.keys():
            existe_error = 1
            error = "Error de Parametros"

        user_id = request.POST['id']
        head = request.POST['head']
        body = request.POST['body']
        payload = {'head': head, 'body': body}

        division_user = user_id.split('|')
        #print('division user: ', division_user, ' head: ', head, ' body: ', body, ' payload: ', payload)

        for user_send in division_user:
            #print('user send: ', user_send)
            user = get_object_or_404(User, pk=int(user_send))

            send_user_notification(user=user, payload=payload, ttl=1000)

        return JsonResponse(status=200, data={"message": "Web push successful"})

    except TypeError:
        return JsonResponse(status=500, data={"message": "Error al enviar"})
