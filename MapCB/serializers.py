from rest_framework import serializers
from MapCB.models import DatiPrezzi

# Serializer per i dati dei prezzi


class PrezziSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatiPrezzi
        fields = ('id',
                  'web_scraper_order',
                  'web_scraper_start_url',
                  'stato',
                  'regione',
                  'provincia',
                  'comune',
                  'indirizzo',
                  'nome_annuncio',
                  'metri_quadri',
                  'prezzo',
                  'affitto_vendita',
                  'data_inserimento',
                  'fascia_prezzo',
                  'latitudine',
                  'longitudine')
