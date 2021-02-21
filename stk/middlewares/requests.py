from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from .constants import URL
from authentication.models import AuthToken

def login_required(function):
    def return_function(request, *args, **kwargs):
        try:
            if request.headers.get("Authorization"):
                token = request.headers.get("Authorization").split(" ")[1]
                tokens = AuthToken.objects.filter(token=token)
                if len(tokens) > 0:
                    tokens = tokens.first()
                    return function(request, *args, **kwargs)
                else:
                    response = redirect(URL + "auth/")
                    return response
            else:
                return redirect(URL + "/auth")

        except Exception as e:
            return redirect(URL + "/auth")

    return return_function

def post_request(function):
    def return_function(request, *args, **kwargs):
        try:
            if(request.method == "POST"):
                return function(request, *args, **kwargs)
            else:
                return JsonResponse({
                    'message': 'Invalid Request!',
                }, status=400)
        except Exception as e:
            repr(e)
            print(e)
            return JsonResponse({
                'message': 'Internal Server Error!'
            }, status=500)

    return return_function