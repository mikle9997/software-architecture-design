from django.shortcuts import render, HttpResponse

sessionUser = {
  'name': 'qzerrty'
}
# sessionUser = None

def index(request):
  context = {
    'logined': sessionUser != None
  }
  if (sessionUser != None):
    context['name'] = sessionUser['name']

  return render(request, 'coliving/index.html', context)

def search(request):
  return render(request, 'coliving/search-co-living.html')

def rent(request):
  return render(request, 'coliving/rent-co-living.html')