# Django Imports
from django.contrib import admin

# Other Imports
from .models import DatiPrezzi

admin.site.site_title = "Amministrazione Crossborder"  # Cambio titolo in alto
admin.site.site_header = "Amministrazione Crossborder"  # Cambio titolo nella tab del browser
admin.site.index_title = "Gestione Sito"  # Cambio titolo nell'index della pagina di amministrazione

admin.site.register(DatiPrezzi) # Aggiunge il modello dei dati all'interfaccia admin così da potervi interagire

admin.site.index_template = "admin/admin_index.html"  # Setta la pagina admin a quella customizzata con i nuovi bottoni
