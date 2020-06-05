from django.shortcuts import render, HttpResponse, redirect
from .AuthBackend import *
from django.contrib.sessions.models import Session
from .models import Request

import json

def index(request):
  # Session.objects.all().delete()
  # ColivingUser.objects.all().delete()
  # Request.objects.all().delete()
  # print(Session.objects.all())
  # print(ColivingUser.objects.all())
  # print(Request.objects.all())

  userLogin = request.session.get('login', None)
  try:
    user = ColivingUser.objects.get(pk = userLogin)
  except:
    userLogin = None

  context = {
    'logined': userLogin != None,
    'name': userLogin,
  }

  return render(request, 'coliving/index.html', context)

def search(request):
  userLogin = request.session.get('login', None)
  try:
    user = ColivingUser.objects.get(pk = userLogin)
  except:
    userLogin = None

  if userLogin == None:
    return redirect('/')

  if request.method == 'GET':
    return render(request, 'coliving/search-co-living.html')
  elif request.method == 'POST':
    req = request.read()
    
    colivings = list(
      filter(lambda x: True, Request.objects.all())
      # filter(lambda x: x.state == 1, Request.objects.all())
    )

    return HttpResponse(json.dumps(list(map(lambda x: {
      'title': x.title,
      'description': x.description,
      'image': x.image.url,
      'adress': x.adress,
    }, colivings))), status=200)

def rent(request):
  userLogin = request.session.get('login', None)
  try:
    user = ColivingUser.objects.get(pk = userLogin)
  except:
    userLogin = None
  
  if request.method == 'GET':
    if userLogin == None:
      return redirect('/')

    return render(request, 'coliving/rent-co-living.html')
  elif request.method == 'POST':
    queryPost = request.POST

    req = Request(
      adress=queryPost.get('adress'),
      description=queryPost.get('description'),
      image=request.FILES['file'],
      state=0,
      user=user
    )
    req.save()

    return HttpResponse(status=200)

def announcemet(request):
  userLogin = request.session.get('login', None)
  try:
    user = ColivingUser.objects.get(pk = userLogin)
  except:
    userLogin = None

  if userLogin == None:
    return redirect('/')

  context = {
    
  }
  return render(request, 'coliving/announcemet.html', context)

def account(request):
  userLogin = request.session.get('login', None)
  try:
    user = ColivingUser.objects.get(pk = userLogin)
  except:
    userLogin = None

  if userLogin == None:
    return redirect('/')


  try:
    requests = list(
        map(
          lambda x: {
            'isWatching': x.state == 0,
            'isOk': x.state == 1,
            'isBad': x.state == 2,
            'title': x.title,
            'description': x.description,
            'image': x.image,
          },
          filter(lambda x: x.user == user, Request.objects.all())
        )
      )
    # print(requests)
  except:
    requests = []
  
  context = {
    'name': userLogin,
    'roleUser': user.role == 1,
    'roleStaff': user.role == 2 or user.role == 3,
    'userFullName': user.name,
    'userPassword': user.password,
    'userContact': user.contact,
    'requests': requests,
  }
  return render(request, 'coliving/account.html', context)

def login(request):
  body = json.loads(request.read())
  
  user = AuthBackend.authenticate(body['login'], body['pass'])
  if user == None:
    return HttpResponse(status=404)
  else:
    request.session['login'] = body['login']
    return HttpResponse(status=200)

def register(request):
  body = json.loads(request.read())
  
  if (AuthBackend.getUser(body['login']) != None):
    return HttpResponse(status=403)

  user = ColivingUser(name=body['name'], login=body['login'], password=body['pass'], contact=body['contact'], role=1)
  user.save()
  request.session['login'] = body['login']
  
  return HttpResponse(status=200)

def logout(request):
  request.session['login'] = None

  return HttpResponse(status=200)

def changeInfo(request):
  try:
    body = json.loads(request.read())

    userLogin = request.session.get('login', None)
    user = ColivingUser.objects.get(pk = userLogin)

    user.name     = body['name']
    user.password = body['password']
    user.contact  = body['contact']
    user.save()

    return HttpResponse(status=200)
  except:
    return HttpResponse(status=403)