from django.shortcuts import render

def index(request):
    return render(request, "main/index.html")

def a(request):
    return render(request, "main/a.html")

def b(request):
    return render(request, "main/b.html")

def c(request):
    return render(request, "main/c.html")

def whale(request):
    return render(request, "main/whale.html")

def whaleride(request):
    return render(request, "main/whaleride.html")
