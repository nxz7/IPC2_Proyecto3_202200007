from django.shortcuts import render

import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render



def myform_view(request):
    if request.method == 'POST':
        data = request.POST.get("data")
        file = request.FILES.get("file")

        if not file:
            return JsonResponse({"message": "No se ha seleccionado un archivo."})

        try:
            # Envía la solicitud al backend de Flask con el archivo adjunto
            files = {"file": (file.name, file.read())}
            response = requests.post('http://127.0.0.1:5000/cargarXml', data={"data": data}, files=files)
            response.raise_for_status()
            # Procesa la respuesta del backend de Flask
            response_data = response.json()
            return JsonResponse(response_data)
        except requests.exceptions.RequestException as e:
            return HttpResponse(str(e), status=500)

    return render(request, 'myform.html')


def myform_view2(request):
    if request.method == 'POST':
        file = request.FILES.get("xml")

        if not file:
            return JsonResponse({"message": "No se ha seleccionado un archivo."})

        try:
            # Envía la solicitud al backend de Flask con el archivo adjunto
            files = {"xml": (file.name, file.read())}
            response = requests.post('http://127.0.0.1:5000/almacenarInfoXml', files=files)
            response.raise_for_status()
            # Procesa la respuesta del backend de Flask
            response_data = response.json()
            return JsonResponse(response_data)
        except requests.exceptions.RequestException as e:
            return HttpResponse(str(e), status=500)

    return render(request, 'myform.html')


def get_users_view(request):
    if request.method == 'GET':
        date_to_check = request.GET.get('date')
        if not date_to_check:
            return JsonResponse({'error': 'No selecciono fecha.'}, status=400)

        try:
            response = requests.get(f'http://127.0.0.1:5000/devolverUsuarios?date={date_to_check}')
            response.raise_for_status()
            response_data = response.json()
            return JsonResponse(response_data, safe=False)
        except requests.exceptions.RequestException as e:
            return HttpResponse(str(e), status=500)

    return render(request, 'myform.html')

def get_hashtags_view(request):
    if request.method == 'GET':
        date_to_check = request.GET.get('date')
        if not date_to_check:
            return JsonResponse({'error': 'No selecciono fecha.'}, status=400)

        try:
            response = requests.get(f'http://127.0.0.1:5000/devolverHashtags?date={date_to_check}')
            response.raise_for_status()
            response_data = response.json()
            return JsonResponse(response_data, safe=False)
        except requests.exceptions.RequestException as e:
            return HttpResponse(str(e), status=500)

    return render(request, 'myform.html')


def classify_messages_view(request):
    if request.method == 'GET':
        date_to_check = request.GET.get('date')
        if not date_to_check:
            return JsonResponse({'error': 'No selecciono fecha.'}, status=400)

        try:
            response = requests.get(f'http://127.0.0.1:5000/clasificarMensajes?date={date_to_check}')
            response.raise_for_status()
            response_data = response.json()
            return JsonResponse(response_data, safe=False)
        except requests.exceptions.RequestException as e:
            return HttpResponse(str(e), status=500)

    return render(request, 'myform.html')

def clear_data_view(request):
    if request.method == 'POST':
        try:
            response = requests.post('http://127.0.0.1:5000/clearData')
            response.raise_for_status()
            response_data = response.json()
            return JsonResponse(response_data)
        except requests.exceptions.RequestException as e:
            return HttpResponse(str(e), status=500)

    return render(request, 'myform.html')