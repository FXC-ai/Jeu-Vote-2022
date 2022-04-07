from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from questions.models import Propositions, RandomPropositions
from django.core.exceptions import ObjectDoesNotExist
from questions.forms import TestForm, PropForm
from django.urls import reverse

import pickle as pk
import random, string

# Create your views here.

def formulaire(request, tok, indice):
    template = loader.get_template('questions/formulaire.html')



    context = {'tok':tok,
               'indice_suiv' : indice+1,
               'indice_prec' : indice-1,
               }

    fileName = 'questions/static/questions/arr_formulaires/' + tok

    if request.method == 'POST':
        file = open(fileName, 'rb')
        arr_prop = pk.load(file)
        file.close()

        form = PropForm(request.POST)
        if form.is_valid():

            arr_prop[indice - 1][1] = form.cleaned_data['note']
            arr_prop[indice - 1][2] = form.cleaned_data['not_imp']

            file = open(fileName, 'wb')
            pk.dump(arr_prop, file)
            file.close()
            print('saved')

        if indice < len(arr_prop):
            context['considered_prop'] = arr_prop[indice][0]
            context['propForm'] = PropForm()
            context['arr_prop'] = arr_prop
        else :
            return redirect('resultat', tok)


    else:
        file = open(fileName, 'rb')
        arr_prop = pk.load(file)
        file.close()

        context['considered_prop'] = arr_prop[indice][0]
        context['propForm'] = PropForm()
        context['arr_prop'] = arr_prop

    return HttpResponse(template.render(context, request))

def resultat(request, tok):
    template = loader.get_template('questions/resultat.html')

    file = open("/home/oem/PycharmProjects/JeuVote/questions/arr_candidats", 'rb')
    arr_candidats = pk.load(file)
    file.close()

    dict_rst = dict()
    for candidat in arr_candidats :
        dict_rst[candidat] = [0,0]

    context = {'tok':tok}

    fileName = 'questions/static/questions/arr_formulaires/' + tok

    file = open(fileName, 'rb')
    arr_prop = pk.load(file)
    file.close()

    context['arr_prop'] = arr_prop

    for prop in arr_prop :
        if prop[2] == False :
            dict_rst[prop[0].candidat][0] += prop[1]
            dict_rst[prop[0].candidat][1] += 1

    for candidat, rst in dict_rst.items() :
        if rst[1] != 0 :
            dict_rst[candidat].append(rst[0] / rst[1])
        else:
            dict_rst[candidat].append(0)

    context['dict_rst'] = dict_rst

    sorted_rst = sorted(dict_rst.items(), key=lambda x: x[1][2], reverse = True)

    context['sorted_rst'] = sorted_rst

    return HttpResponse(template.render(context, request))

def form_creator (request):

    tok = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

    file = open("/home/oem/PycharmProjects/JeuVote/questions/arr_candidats", 'rb')
    arr_candidats = pk.load(file)
    file.close()

    file = open("/home/oem/PycharmProjects/JeuVote/questions/arr_sections", 'rb')
    arr_sections = pk.load(file)
    file.close()

    list_rand_pr = list()
    for section in arr_sections:
        list_temp_pr = list()
        for candidat in arr_candidats:
            req = Propositions.objects.filter(candidat=candidat).filter(section=section)
            if req:
                pp = random.choice(req)
                list_temp_pr.append([pp,0,False])

        random.shuffle(list_temp_pr)
        list_rand_pr+=list_temp_pr


    list_to_save = list_rand_pr


    fileName = 'questions/static/questions/arr_formulaires/' + tok
    file = open(fileName, 'wb')
    pk.dump(list_to_save, file)
    file.close()

    return redirect('formulaire', tok , 0)

def propositions_deleteAll(request):
    print('Processus de supression de la database')

    for pr in Propositions.objects.all():
        print('supression id', pr.id)
        pr.delete()

    return HttpResponse('Tout est supprimé')

def propositions_addAll(request):
    print('debut du processus')
    file = open("/home/oem/PycharmProjects/JeuVote/questions/df_proposition", 'rb')
    df_propositions = pk.load(file)
    file.close()

    list_test = list()
    for prop in df_propositions.iterrows():
        print(prop)
        list_test.append([prop[1]['Proposition'], prop[1]['Theme'], prop[1]['Section'], prop[1]['Candidat']])

        proposition = Propositions(proposition=prop[1]['Proposition'], theme=prop[1]['Theme'], section = prop[1]['Section'], candidat=prop[1]['Candidat'])
        proposition.save()

    return HttpResponse('Tout est ok {}'.format(list_test))

def propositions_id(request, id):

    print('id URL = ', id)

    try :
        req2 = Propositions.objects.get(id=id)
        resultat = req2.proposition
    except ObjectDoesNotExist :
        return HttpResponse(status = 404)

    return HttpResponse('Résultat : {} '.format(resultat))
