from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def accueil (request):
    template = loader.get_template('accueil/index.html')
    context = {}
    return HttpResponse(template.render(context, request))



