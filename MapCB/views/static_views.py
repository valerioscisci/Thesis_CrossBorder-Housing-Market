# Django Imports
from django.shortcuts import render
from django.views.generic import TemplateView

# Vista per l'homepage

class HomepageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'homepage.html', context=None)
