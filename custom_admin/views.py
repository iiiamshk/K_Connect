from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse

import json, requests

# Create your views here.
def get_authToken(request):
    if request.COOKIES.get('authToken'):
        return {"authToken": request.COOKIES.get('authToken')}


def home(request):
    if not get_authToken(request): 
        return redirect('login')

    resp =  requests.get('http://127.0.0.1:8000/api/account/', cookies= get_authToken(request))

    return render(request, 'cAdmin/home.html',{'data': resp.json()})


def login_view(request):
    if get_authToken(request):
        return redirect('admin_home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        resp = requests.post('http://127.0.0.1:8000/api/login/', data={
            'email': email,
            'password': password
        })
        return JsonResponse({'data': resp.json(), 'status': resp.status_code})
    
    return render(request, 'cAdmin/login.html')


def login_verify(request):
    if get_authToken(request):
        return redirect('admin_home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')

        resp = requests.post('http://127.0.0.1:8000/api/login/verify/', data={
            'email': email,
            'otp': otp
        })

        response = JsonResponse({'data': resp.json(), 'status': resp.status_code})
        if resp.status_code == 200:
            response.set_cookie(
                'authToken', resp.json()['authToken'],
                httponly=True,
                secure=False,   # Use True in production for HTTPS
                samesite='Strict',
                max_age=3600
            )
        return response 

def logout_view(request):
    if not get_authToken(request):
        return redirect('login')
    
    if request.method == 'POST':        
        resp = requests.post('http://127.0.0.1:8000/api/logout/', cookies= get_authToken(request))
        response = JsonResponse({'data': resp.json(), 'status': resp.status_code})
        response.delete_cookie('authToken')
        return redirect('admin_login')
    return redirect('admin_home')

def account_view(request):
    if not get_authToken(request):
        return redirect('login')

    resp =  requests.get('http://127.0.0.1:8000/api/account/', cookies= get_authToken(request))
    return render(request, 'cAdmin/account.html',{'data': resp.json()})

def group_view(request):
    if not get_authToken(request):
        return redirect('login')
    
    resp =  requests.get('http://127.0.0.1:8000/api/group/', cookies= get_authToken(request))
    return render(request, 'cAdmin/group.html',{'groups': resp.json()})