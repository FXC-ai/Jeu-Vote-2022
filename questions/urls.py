

from django.urls import path, include

import questions.views

urlpatterns = [
    path('formulaire/delAll/', questions.views.propositions_deleteAll),
    path('formulaire/addAll/', questions.views.propositions_addAll),
    path('formulaire/<str:tok>/<int:indice>/', questions.views.formulaire, name = 'formulaire'),
    path('formulaire/formCreator/', questions.views.form_creator, name = 'form_creator'),
    path('formulaire/resultat/<str:tok>/', questions.views.resultat, name = 'resultat'),
    path('id/<int:id>/', questions.views.propositions_id),
]
