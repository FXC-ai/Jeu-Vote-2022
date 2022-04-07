
from django.contrib import admin
from django.urls import path
from django.urls import register_converter

import accueil.views
import accueil.converters

register_converter(accueil.converters.TwoDigitDayConverter, 'dd')

urlpatterns = [
    path('', accueil.views.accueil, name = 'accueil'),

]
