from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy

from .models import DatiPrezzi

admin.site.site_title = "Amministrazione Crossborder"
admin.site.site_header = "Amministrazione Crossborder"
admin.site.index_title = "Gestione Sito"

admin.site.register(DatiPrezzi)

admin.site.index_template = "admin/admin_index.html"  # Setta la pagina admin a quella customizzata
