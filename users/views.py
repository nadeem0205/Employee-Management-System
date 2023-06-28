from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User 

@csrf_exempt
def register(request):
    """
    API to handle user registration which accepts,
    username, password, email and returns the JSON response
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if username and password and email:
            user = User.objects.create_user(username=username, password=password, email=email)
            return JsonResponse({'message': 'Registration successful.'})
        else:
            return JsonResponse({'message': 'Invalid data.'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)

@csrf_exempt
def user_login(request):
    """
    API to handle user login which accepts,
    username and password and returns the JSON response
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            session_key = request.session.session_key
            if session_key is None:
                request.session.save()
                session_key = request.session.session_key
            return JsonResponse({'message': 'Login successful.', 'session_key': session_key})
        else:
            return JsonResponse({'message': 'Invalid credentials.'}, status=401)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)

@csrf_exempt
def user_logout(request):
    # API For user logout and returns JSON response
    logout(request)

    return JsonResponse({'message': 'Logout successful.'})