from django.shortcuts import render


def home(request):
    return render(request, 'catequesis/home.html')