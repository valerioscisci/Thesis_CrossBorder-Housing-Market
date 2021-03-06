from rest_framework import serializers
from MapCB.models import DatiPrezzi

# Serializer per i dati dei prezzi


class PrezziSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatiPrezzi
        fields = ('web_scraper_order',
                  'web_scraper_start_url',
                  'stato',
                  'regione',
                  'provincia',
                  'comune',
                  'zip_code',
                  'indirizzo',
                  'nome_annuncio',
                  'metri_quadri',
                  'prezzo',
                  'affitto_vendita',
                  'data_inserimento',
                  'fascia_prezzo',
                  'latitudine',
                  'longitudine')

class DuplicatiSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatiPrezzi
        fields = ('nome_annuncio',
                  'stato',
                  'regione',
                  'provincia',
                  'comune',
                  'indirizzo',
                  'metri_quadri',
                  'prezzo')

class PrezziMediSerializer(serializers.ModelSerializer):
    num_annunci = serializers.IntegerField()
    prezzo_medio = serializers.FloatField()

    class Meta:
        model = DatiPrezzi
        fields = ('stato',
                  'provincia',
                  'affitto_vendita',
                  'fascia_prezzo',
                  'num_annunci',
                  'prezzo_medio')
