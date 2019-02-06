from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, friend. You're at the realpolitik index.")

def load_user(request, user = "nati"):
    return HttpResponse("Hello, " + user + ". This is your map.")
