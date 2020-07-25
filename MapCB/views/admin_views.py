# Django Imports

from django.contrib import messages
from django.shortcuts import render

# Other Imports
import io
import re
import csv

# Models Imports
from MapCB.models import DatiPrezzi


# Vista che si occupa di caricare i dati nel DB dal file csv inserito dall'admin


def upload_dati(request):
    # Dichiaro il template che contiene il form di upload
    template = "admin/admin_upload.html"
    #dati_prezzi = DatiPrezzi.objects.all()

    # Variabile che mi contiene l'ordine delle colonne del .csv e i dati dei prezzi già caricati
    prompt = {
        'order': 'Le colonne del csv devono essere le seguenti: web-scraper-order,web-scraper-start-url, '
                 'indirizzo, nome_annuncio, metri, price',
        #'dati_prezzi': dati_prezzi
    }

    # Se la richiesta è una GET i valori dei prezzi in base alla chiave specificata.
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['csv_prezzi']

    # Check per vedere se il file caricato è un csv
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'Errore file, caricare esclusivamente file csv!')
    data_set = csv_file.read().decode('UTF-8')

    # Uso uno stream per leggere le righe del file una alla volta per poi caricare i dati nel DB
    io_string = io.StringIO(data_set)
    next(io_string)  # Salto l'header
    for row in io_string:
        # Nel caso non riesce a leggere una riga prosegue con la prossima
        try:
            row.replace('\"\"', '\"')  # Rimpiazza le coppie di doppi apici con uno solo
            columns = row.split(',"')  # Splitta le righe in tante colonne

            # Elimina i numeri dopo la virgola e tutti i caratteri non numerici
            metri = re.sub(r"[^\d]", "", columns[4].split(',', 1)[0])
            price = re.sub(r"[^\d]", "", columns[5].split(',', 1)[0])
        except IndexError:
            continue

        # Se c'è stato un errore nell'inserimento dei  metri allora salto la riga
        if len(metri) > 4 or metri == price:
            continue

        # Creo un'occorrenza dei dati raccolti dalla riga all'interno del database
        _ = DatiPrezzi.objects.create(
            web_scraper_order=columns[0].replace('"', ''),
            web_scraper_start_url=columns[1].replace('"', ''),
            stato='',
            regione='',
            provincia='',
            comune='',
            indirizzo=columns[2].replace('"', ''),
            nome_annuncio=columns[3].replace('"', ''),
            metri_quadri=metri if metri != '' else -1.0,
            prezzo=price if price != '' else -1.0,
            affitto_vendita='',
            fascia_prezzo='',
            latitudine=0,
            longitudine=0
        )
    context = {}
    return render(request, template, context)
