# Django Imports
from django.shortcuts import render
from django.views.generic import TemplateView

# Vista per la mappa

class MappaView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'mappa.html', context=None)

