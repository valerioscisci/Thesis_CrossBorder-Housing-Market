# Django Imports
from django.db import models
from django.utils.translation import gettext as _
from django.db.models import DecimalField
# Other Imports

# Classe che definisce il modello per la Collection che conterrà i dati dei prezzi


class DatiPrezzi(models.Model):
    web_scraper_order = models.CharField(max_length=20, blank=False, default='')
    web_scraper_start_url = models.CharField(max_length=300, blank=False, default='')
    stato = models.CharField(max_length=20, blank=False, default='')
    regione = models.CharField(max_length=30, blank=False, default='')
    provincia = models.CharField(max_length=20, blank=False, default='')
    comune = models.CharField(max_length=20, blank=False, default='')
    zip_code = models.CharField(max_length=20, blank=False, default='')
    indirizzo = models.CharField(max_length=100, blank=False, default='')
    nome_annuncio = models.CharField(max_length=500, blank=False, default='')
    metri_quadri = models.IntegerField(blank=False, default=-1)
    prezzo = models.IntegerField(blank=False, default=-1)
    affitto_vendita_choices = (
        ('A', 'Affitto'),
        ('V', 'Vendita'),
    )
    affitto_vendita = models.CharField(max_length=1, choices=affitto_vendita_choices)
    data_inserimento = models.DateField(_("Date"), auto_now_add=True)
    fascia_prezzo_choices = (
        ('B', 'Bassa'),
        ('M', 'Media'),
        ('A', 'Alta'),
    )
    fascia_prezzo = models.CharField(max_length=1, choices=fascia_prezzo_choices)
    latitudine = DecimalField(max_digits=9, decimal_places=6)
    longitudine = DecimalField(max_digits=9, decimal_places=6)
