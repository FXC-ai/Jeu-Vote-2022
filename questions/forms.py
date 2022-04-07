from django import forms
from questions.models import Propositions

import pickle as pk
import random

class PropForm(forms.Form):

    note = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'range', 'step': '1', 'min': '0', 'max': '10'}),
                                  required=True, label= 'note')
    not_imp = forms.BooleanField(required=False, label='Pas important')



class TestForm(forms.Form):

    CITIES_CHOICE = (
        (0, 'Martigny'),
        (1, 'Chamonix'),
        (2, 'Saint-Gervais'),
        (3, 'Champoussin'),
        (4, 'Niort'),
        (5, 'Poitiers'),
        (6, 'Saint-Varent'),
        (7, 'Vivonne'),
        (8, 'Iteuil')
    )

    name = forms.CharField(label = 'Your name', max_length=255)
    email = forms.EmailField(label='Your email', max_length=255, required = False)
    yes_no = forms.BooleanField(label = 'Either Yes or No')
    city = forms.ChoiceField(label = 'Your city', choices=CITIES_CHOICE)
    note = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'step': '1', 'min': '0', 'max': '10'}), required=True)