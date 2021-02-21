from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from middlewares.requests import *

# Create your views here.
@csrf_exempt
@login_required
def get_users(request, *args, **kwargs):
    return JsonResponse({
        'message': "Here are the List of users!"
    })