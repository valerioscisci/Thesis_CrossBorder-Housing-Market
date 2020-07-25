from django.contrib import admin
from .models import DatiPrezzi


admin.site.register(DatiPrezzi)

admin.site.index_template = "admin/admin_index.html"  # Setta la pagina admin a quella customizzata
