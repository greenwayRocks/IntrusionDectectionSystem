from django.shortcuts import render

# Create your views here.
def home(request):
    context = { 'a': 'HelloWorld!' }
    return render(request, 'index.html', context)
