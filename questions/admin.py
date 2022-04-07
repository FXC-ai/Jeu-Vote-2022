from django.contrib import admin

from questions.models import Propositions

class PropositionsAdmin(admin.ModelAdmin):
    list_display = ('candidat', 'proposition', 'section', 'theme')
    list_filter = ('candidat', 'section')
    search_fields = ['proposition']

admin.site.register(Propositions, PropositionsAdmin)
