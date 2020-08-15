# Django Imports
from django.contrib import messages
from django.db.models import Max, Count
from django.shortcuts import render

# Other Imports
import io
import re
from currency_converter import CurrencyConverter
from geopy.geocoders import Nominatim

# Models Imports
from MapCB.models import DatiPrezzi

# Funzione che elimina gli annunci duplicati che sono stati inseriti e mantiene pulito il database
from MapCB.serializers import DuplicatiSerializer


def rimuovi_duplicati():
    # Mi preparo un json vuoto che mi tornerà i duplicati trovati e
    response_data = {}

    # Mi preparo un array che indica i campi che verranno valutati per trovare i duplicati
    unique_fields = ['nome_annuncio', 'stato', 'regione', 'provincia', 'comune', 'indirizzo', 'metri_quadri', 'prezzo']

    # Trova i duplicati
    duplicates = (
         DatiPrezzi.objects.values(*unique_fields)
        .order_by()
        .annotate(max_id=Max('_id'), count_id=Count('_id'))
        .filter(count_id__gt=1)
    )

    # Per ogni duplicato prova a rimuoverlo, se qualcosa va storto ritorna un messaggio di errore
    try:
        for duplicate in duplicates:
            (
                DatiPrezzi.objects
                .filter(**{x: duplicate[x] for x in unique_fields})
                .exclude(_id=duplicate['max_id'])
                .delete()
            )
        response_data["rimossi"] = "Vero"
    except:
        response_data["rimossi"] = "falso"

    # Mi serializzo i duplicati che sono stati trovati cosi li mostro all'admin
    duplicati_serializer = DuplicatiSerializer(duplicates, many=True)

    # Preparo i duplicati per tornarli alla vista chiamante
    response_data["duplicati"] = duplicati_serializer.data

    return response_data


# Vista che si occupa di caricare i dati nel DB dal file csv inserito dall'admin


def upload_dati(request):
    # Dichiaro il template che contiene il form di upload
    template = "admin/admin_upload.html"

    # Variabile che mi contiene l'ordine delle colonne del .csv e i dati dei prezzi già caricati
    prompt = {
        'order': 'Le colonne del csv devono essere le seguenti: web-scraper-order,web-scraper-start-url, '
                 'indirizzo, nome_annuncio, metri, price'
    }

    # Se la richiesta è una GET i valori dei prezzi in base alla chiave specificata.
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['csv_prezzi']

    # Check per vedere se il file caricato è un csv
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'Errore file, caricare esclusivamente file csv!')
    data_set = csv_file.read().decode('UTF-8')

    # Mi preparo una variabile per comunicare all'admin se tutto è stato caricato correttamente
    error = False

    # Uso uno stream per leggere le righe del file una alla volta per poi caricare i dati nel DB
    io_string = io.StringIO(data_set)
    next(io_string)  # Salto l'header
    for row in io_string:
        # Nel caso non riesce a leggere una riga prosegue con la prossima
        try:
            row.replace('\"\"', '\"')  # Rimpiazza le coppie di doppi apici con uno solo
            columns = row.split(',"')  # Splitta le righe in tante colonne
            print(columns)
            # Elimina i numeri dopo la virgola e tutti i caratteri non numerici
            metri = re.sub(r"[^\d]", "", columns[4].split(',', 1)[0])
            price = re.sub(r"[^\d]", "", columns[5].split(',', 1)[0])
            if price == '':
                price = -1
            if metri == '':
                metri = -1
            
        except IndexError:
            error = True
            continue

        # Se c'è stato un errore nell'inserimento dei  metri allora salto la riga
        if len(str(metri)) > 4 or metri == price:
            error = True
            continue

        # Mi costruisco un geolocator per poi usarlo per avere informazioni sulla localizzazione della casa
        geolocator = Nominatim(user_agent="crossborderapp")

        # Mi trovo la location con il geolocator creato prima e nel caso non ho il comune uso la provincia
        location = geolocator.geocode(columns[2])

        # Mi prendo dal file lo stato e la regione sicuramente e se c'è anche la provincia
        stato_regione_provincia = csv_file.name.replace('.csv', '').split('_')

        stato = stato_regione_provincia[1]  # All'indice 0 c'è la stringa 'dati'
        regione = stato_regione_provincia[2]
        try:
            provincia = stato_regione_provincia[3]
        except IndexError:
            # Caso Svizzera
            provincia = location.raw['display_name'].split(', ', 2)[1]

        # Nel caso in cui non ho il comune in colonna 3, allora provo ad usare la provincia per estrarre long e lat
        location_riserva = geolocator.geocode(provincia)

        # Assegno i valori di latitudine e longitudine in base all'indirizzo trovato
        try:
            latitudine = location.latitude
            longitudine = location.longitude
        except:
            try:
                latitudine = location_riserva.latitude
                longitudine = location_riserva.longitude
            except:
                latitudine = longitudine = 0

        # Mi trovo il comune se coincide con la provincia, altrimenti me lo cerco nell'indirizzo
        columns[2] = columns[2].replace('"', '')
        if stato == 'austria' or stato == 'svizzera':
            if columns[2][0].isdigit():
                comune_zipcode = columns[2].split(' ', 1)
            else:
                try:
                    comune_zipcode = columns[2].split(',', 1)[1][:1].split(' ', 1)
                except:
                    comune_zipcode = ['', '']

            zipcode = comune_zipcode[0]
            comune = comune_zipcode[1]
        elif stato == 'francia' or stato == 'italia':
            comune = columns[2]

            try:
                zipcode = geolocator.reverse((latitudine, longitudine)).raw['address']['postcode']
            except:
                zipcode = 0
        elif stato == 'slovenia':
            pattern = re.compile("\d{2}\. \d{2}")
            if pattern.match(columns[2]):
                comune = provincia
            else:
                comune = columns[2]

            try:
                zipcode = geolocator.reverse((latitudine, longitudine)).raw['address']['postcode']
            except:
                zipcode = 0

        # Mi creo una variabile di appoggio per contenere l'int del prezzo
        price_int = int(price)

        # Per trovare valore in euro del prezzo delle case svizzere espresso in franchi svizzeri
        if price != -1.0 and stato == 'svizzera':
            c = CurrencyConverter()
            converted_price = int(c.convert(price_int, 'EUR'))
            print(converted_price)
            price = converted_price

        # Vedo se si tratta di una casa in affitto o in vendita
        if price_int > 9999:
            affitto_vendita = 'V'
        else:
            affitto_vendita = 'A'

        # Mi setto la fascia di prezzo in base al fatto che sia una casa in affitto o in vendita

        if affitto_vendita == 'V':
            if price_int < 125000:
                fascia_prezzo = 'B'
            elif 125000 <= price_int < 200000:
                fascia_prezzo = 'M'
            else:
                fascia_prezzo = 'A'
        else:
            if price_int < 600:
                fascia_prezzo = 'B'
            elif 600 <= price_int < 1200:
                fascia_prezzo = 'M'
            else:
                fascia_prezzo = 'A'

        # Creo un'occorrenza dei dati raccolti dalla riga all'interno del database
        _ = DatiPrezzi.objects.create(
            web_scraper_order=columns[0].replace('"', ''),
            web_scraper_start_url=columns[1].replace('"', ''),
            stato=stato,
            regione=regione,
            provincia=provincia,
            comune=comune,
            zip_code=zipcode,
            indirizzo=columns[2].replace('"', ''),
            nome_annuncio=columns[3].replace('"', ''),
            metri_quadri=metri,
            prezzo=price,
            affitto_vendita=affitto_vendita,
            fascia_prezzo=fascia_prezzo,
            latitudine=latitudine,
            longitudine=longitudine
        )

    # Prima di terminare la procedura, controlla se ci sono dei duplicati e gli elimina
    response_rimozione = rimuovi_duplicati()
    prompt["lista_duplicati"] = response_rimozione['duplicati']
    prompt["conferma_rimossi"] = response_rimozione['rimossi']
    prompt["error"] = error
    context = prompt

    return render(request, template, context)
