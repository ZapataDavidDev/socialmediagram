"""Socialmediagram views."""

# Django
from django.http import HttpResponse
from django.shortcuts  import render

# Utilities
from datetime import datetime
import json

# Forms
from users.forms import ProfileSerch

# Models
from users.models import Profile


#def atletico_nacional(request):
#    """Return a greeting."""
#    return HttpResponse('El Verde! El más grande de colombia!. Hora del servidor donde corre la app {now}'.format(
#        now=datetime.now().strftime('%b %dth, %Y - %H:%M hrs')
#    ))

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_http_methods(["GET", "POST"])
def atletico_nacional(request):
    """
    Vista que puede recibir datos en formato JSON y devuelve una respuesta 200.
    Soporta tanto GET como POST.
    """
    if request.method == 'POST':
        try:
            # Intentar parsear el body como JSON
            if request.body:
                data = json.loads(request.body)
            else:
                data = {}
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON format'
            }, status=400)

        # Procesar los datos recibidos
        response_data = {
            'status': '200',
            'message': 'Data received successfully',
            'received_data': data,
            'greeting': 'El Verde! El más grande de colombia!'
        }

        return JsonResponse(response_data, status=200)

    else:  # GET
        # Para requests GET, devolver una respuesta simple
        return JsonResponse({
            'status': 'ok',
            'message': 'Atletico Nacional endpoint is ready',
            'greeting': 'El Verde! El más grande de colombia!',
            'method': 'GET'
        }, status=200)

def sort_integers(request):
    """Return a JSON response with sorted integers."""
    numbers = [int(i) for i in request.GET['numbers'].split(',')]
    sorted_ints = sorted(numbers)
    data = {
        'status': 'ok',
        'numbers': sorted_ints,
        'message': 'Integers sorted successfully.'
    }
    return HttpResponse(
        json.dumps(data, indent=4),
        content_type='application/json'
    )


def say_hi(request, name, equipo):
    """Return a greeting."""
    if str(equipo).lower() != 'nacional':
        message = 'Sorry {}, you are not allowed here'.format(name)
    else:
        message = 'Hello, {}! Welcome to socialmediagram'.format(name)
    return HttpResponse(message)


