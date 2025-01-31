from django.shortcuts import render
from django.shortcuts import HttpResponse


def index(request):
    return HttpResponse("Pagrindinis autoserviso puslapis, autoserviso homepage")


def cars(request):
    return HttpResponse("Cia yra autoserviso puslapio, cars skyrelis")
