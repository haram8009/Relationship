from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import auth

def signup(request):
  if request.method == 'POST':
    if request.POST['password1'] == request.POST['password2']:
      user = User.objects.create_user(
        username=request.POST['username'],
        password=request.POST['password1'],
        email=request.POST['email'],
        ) # user는 장고에서 세이브를 자동으로 해줌
      profile = Profile(
        user=user, 
        nickname=request.POST['nickname'],
        image=request.FILES.get('image'),
        )
      profile.save() # 이건 우리가 만든거라 자동으로 세이브 안해줌

      auth.login(request, user)
      return redirect('/')
    return render(request, 'signup.html') # 패스워드가 같지 않을 때
  return render(request, 'signup.html') #포스트 요청이 아닐 때

def login(request):
  if request.method == 'POST':
    username=request.POST['username']
    password=request.POST['password1']
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
      auth.login(request, user)
      return redirect('/')
    return render(request, 'login.html')
  return render(request, 'login.html')

def logout(request):
  auth.logout(request)
  return redirect('/')