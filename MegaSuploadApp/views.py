from django.shortcuts import render


# Create your views here.

# Temporary render
def index(request):
    return render(request, 'index.html', )
