from django.shortcuts import render

def index(request):
    return render(request,"package_system/index.html")
