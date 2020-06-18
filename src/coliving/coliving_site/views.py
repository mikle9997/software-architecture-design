from django.shortcuts import render, HttpResponse, redirect
from .AuthBackend import *
from django.contrib.sessions.models import Session
from .models import Request

import json
import re
import random

def index(request):
      ### !!! WARNING !!! ###

  # Session.objects.all().delete()
  # ColivingUser.objects.all().delete()
  # Request.objects.all().delete()

      ### !!! WARNING !!! ###

  # print(Session.objects.all())
  print(ColivingUser.objects.all())
  print(Request.objects.all())

  userLogin = request.session.get('login', None)
  try:
    user = ColivingUser.objects.get(pk = userLogin)
  except:
    user = None

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
    user = None

  if userLogin == None:
    return redirect('/')

  if request.method == 'GET':
    return render(request, 'coliving/search-co-living.html')
  elif request.method == 'POST':
    req = request.read()
    
    colivings = list(
      filter(
        lambda x: x.state == 1 and re.search(re.compile(req.decode("utf-8"), re.IGNORECASE), 
          str(x.title) + " " + str(x.description) + " " + str(x.adress)),
      Request.objects.all())
    )

    return HttpResponse(json.dumps(list(map(lambda x: {
      'id': x.id,
      'title': x.title,
      'description': x.description,
      'image': x.image.url,
      'adress': x.adress,
    }, colivings))), status=200)

def getConsultant(request):
  userLogin = request.session.get('login', None)
  try:
    user = ColivingUser.objects.get(pk = userLogin)
  except:
    user = None

  if userLogin == None:
    return HttpResponse(status=403)

  return HttpResponse(json.dumps(random.choice(
    list(
      map(
        lambda x: {'name': x.name, 'contact': x.contact}, 
        filter(lambda x: x.isConsultant(), ColivingUser.objects.all())
      )
    )
  )), status=200)

def rent(request):
  userLogin = request.session.get('login', None)
  try:
    user = ColivingUser.objects.get(pk = userLogin)
  except:
    user = None
  
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
      user=user,
      freeSpaces=0
    )
    req.save()

    return HttpResponse(status=200)

def announcemet(request, id=0):
  userLogin = request.session.get('login', None)
  try:
    user = ColivingUser.objects.get(pk = userLogin)
  except:
    return redirect('/')

  try:
    req = Request.objects.get(pk = id)
  except:
    return redirect('/')
  
  if not req.state == 1 and (user.isUser() and not req.user == user):
    return redirect('/')

  context = {
    'title': req.title,
    'description': req.description,
    'image': req.image.url,
    'adress': req.adress,
    'contact': req.organizer.contact,
    'name': req.organizer.name,
    'freespaces': req.freeSpaces,
    'isThisOrganizer': req.organizer == user,
    'ownerName': req.user.name,
    'ownerContact': req.user.contact,
    'isOwner': req.user == user,
    'hasProject': False
  }

  if req.project:
    context['hasProject'] = True
    context['projectFile'] = req.project.url

  return render(request, 'coliving/announcemet.html', context)

def account(request):
  userLogin = request.session.get('login', None)
  try:
    user = ColivingUser.objects.get(pk = userLogin)
  except:
    user = None

  if userLogin == None:
    return redirect('/')

  try:
    requests = list(
        map(
          lambda x: {
            'stateText': 'Одобрено' if x.state == 1 else 'Отклонено' if x.state == 2 else 'На рассмотрении' if x.state == 0 else 'Реализация проекта',
            'stateClass': 'submit' if x.state == 1 else 'cancel' if x.state == 2 else 'watching',
            'title': x.title,
            'adress': x.adress,
            'description': x.description,
            'image': x.image,
            'id': x.id
          }, filter(lambda x: 
            x.user == user
            or user.isAdmin()
            or (user.isOrganizer() and x.state == 0)
            or user.isConsultant(),
          Request.objects.all())
        )
      )
  except:
    requests = []

  accounts = []
  if user.isAdmin():
    accounts = list(
      map(
        lambda x: {
          'name': x.name,
          'login': x.login,
          'contact': x.contact,
          'isUser': x.isUser(),
          'isOrganizer': x.isOrganizer(),
          'isConsultant': x.isConsultant(),
        }, filter(lambda x: not x.isAdmin(), ColivingUser.objects.all()))
    )
  
  acceptedRequests = []
  if user.isConsultant() or user.isOrganizer():
    acceptedRequests = list(
        map(
          lambda x: {
            'stateText': 'Одобрено' if x.state == 1 else 'Отклонено' if x.state == 2 else 'На рассмотрении' if x.state == 0 else 'Реализация проекта',
            'stateClass': 'submit' if x.state == 1 else 'cancel' if x.state == 2 else 'watching',
            'title': x.title,
            'adress': x.adress,
            'description': x.description,
            'image': x.image,
            'id': x.id,
            'name': x.user.name,
            'contact': x.user.contact,
          }, filter(lambda x: user.isOrganizer() and x.organizer == user,
          Request.objects.all())
        )
      )
  
  context = {
    'name': userLogin,
    'roleUser': user.isUser(),
    'roleStaff': user.isOrganizer() or user.isConsultant() or user.isAdmin(),
    'roleOrganizer': user.isOrganizer(),
    'userFullName': user.name,
    'userPassword': user.password,
    'userContact': user.contact,
    'requests': requests,
    'isSuper': user.isAdmin(),
    'accounts': accounts,
    'accepted': acceptedRequests
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
  
  if AuthBackend.getUser(body['login']) != None:
    return HttpResponse(status=403)

  user = ColivingUser(name=body['name'], login=body['login'], password='', contact=body['contact'], role=1)
  user.setHashedPassword(body['pass'])
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
    user.setHashedPassword(body['password'])
    user.contact  = body['contact']
    user.save()

    return HttpResponse(status=200)
  except:
    return HttpResponse(status=403)

def admin(request, action = '', actionLogin = ''):
  userLogin = request.session.get('login', None)
  try:
    user = ColivingUser.objects.get(pk = userLogin)
  except:
    user = None

  if userLogin == None or not user.isAdmin():
    return redirect('/')
  
  if action == 'delete':
    login = json.loads(request.read())['login']
    try:
      ColivingUser.objects.get(pk=login).delete()
      return HttpResponse(status=200)
    except:
      return HttpResponse(status=403)
  elif action == 'create':
    if request.method == 'GET':
      context = {
        'isChanging': False,
        'login': '',
        'name': '',
        'password': '',
        'contact': '',
        'isUser': False,
        'isConsultant': False,
        'isOrganizer': False
      }
      return render(request, 'coliving/accsettings.html', context)
    elif request.method == 'POST':
      queryPost = request.POST

      if AuthBackend.getUser(queryPost.get('login')) != None:
        return HttpResponse(status=403)

      userAcc = ColivingUser(
        name     = queryPost.get('name'),
        login    = queryPost.get('login'),
        password = '',
        contact  = queryPost.get('contact'),
        role     = queryPost.get('role')
      )
      userAcc.setHashedPassword(queryPost.get('password'))
      userAcc.save()

      return HttpResponse(status=200)
  elif action == 'change':
    if request.method == 'GET':
      actionUser = AuthBackend.getUser(actionLogin)

      if actionUser == None:
        return redirect('/')

      context = {
        'isChanging': True,
        'login': actionLogin,
        'name': actionUser.name,
        'password': actionUser.password,
        'contact': actionUser.contact,
        'isUser': actionUser.isUser(),
        'isConsultant': actionUser.isConsultant(),
        'isOrganizer': actionUser.isOrganizer()
      }

      return render(request, 'coliving/accsettings.html', context)
    elif request.method == 'POST':
      actionUser = AuthBackend.getUser(actionLogin)

      queryPost = request.POST

      actionUser.name     = queryPost.get('name')
      actionUser.password = queryPost.get('password')
      actionUser.contact  = queryPost.get('contact')
      actionUser.role     = queryPost.get('role')
      actionUser.save()
      
      return HttpResponse(status=200)

  return HttpResponse(status=200)

def chooseRequest(request):
  userLogin = request.session.get('login', None)
  try:
    user = ColivingUser.objects.get(pk = userLogin)
  except:
    user = None

  if userLogin == None or (not user.isConsultant() and not user.isOrganizer()):
    return redirect('/')

  body = json.loads(request.read())

  try:
    req = Request.objects.get(pk=body['id'])
  except:
    return redirect('/')

  req.organizer = user
  req.state = 4
  req.save()

  return HttpResponse(status=200)


def requestEditing(request, id=0):
  userLogin = request.session.get('login', None)
  try:
    user = ColivingUser.objects.get(pk = userLogin)
  except:
    user = None

  if userLogin == None or (not user.isConsultant() and not user.isOrganizer()):
    return redirect('/')

  try:
    req = Request.objects.get(pk=id)
  except:
    return redirect('/')

  if request.method == 'GET':

    stateOptions = list(map(lambda x: x.update({'selected': 'selected' if x['value'] == req.state else ''}) or x, [
      {'text': 'На рассмотрении', 'value': 4},
      {'text': 'Одобрено', 'value': 1},
      {'text': 'Отклонено', 'value': 2}
    ]))

    context = {
      'title': req.title,
      'image': req.image.url,
      'adress': req.adress,
      'description': req.description,
      'stateOptions': stateOptions,
      'freespaces': req.freeSpaces,
      'hasProject': False
    }

    if req.project:
      context['hasProject'] = True
      context['project'] = req.project.name
    
    return render(request, 'coliving/requestediting.html', context)
  elif request.method == 'POST':
    queryPost = request.POST

    try:
      req.image = request.FILES['file']
    except:
      pass
    try:
      req.project = request.FILES['project']
    except:
      pass
    req.title       = queryPost.get('title')
    req.adress      = queryPost.get('adress')
    req.description = queryPost.get('description')
    req.state       = int(queryPost.get('state'))
    req.freeSpaces  = int(queryPost.get('freespaces'))
    req.save()

    return HttpResponse(status=200)
  

def deleteRequest(request):
  userLogin = request.session.get('login', None)
  try:
    user = ColivingUser.objects.get(pk = userLogin)
  except:
    user = None

  if userLogin == None:
    return HttpResponse(status=403)

  try:
    req = Request.objects.get(pk=json.loads(request.read())['id'])
  except:
    return HttpResponse(status=403)

  if req.user == user:
    req.delete()
    return HttpResponse(status=200)
  else:
    return HttpResponse(status=403)