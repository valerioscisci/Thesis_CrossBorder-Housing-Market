# Django Imports
from django.db.models import Count, Avg
from django.http.response import JsonResponse
from rest_framework.decorators import api_view

# Other Imports
from MapCB.serializers import PrezziSerializer, PrezziMediSerializer
from MapCB.models import DatiPrezzi

# API che mi torna tutti la lista di prezzi presente nel DB
@api_view(['GET', 'POST', 'DELETE'])
def lista_prezzi(request):
    if request.method == 'GET':
        prezzi = DatiPrezzi.objects.exclude(prezzo=-1)

        prezzi_serializer = PrezziSerializer(prezzi, many=True)
        return JsonResponse(prezzi_serializer.data, safe=False)
        # 'safe=False' for objects serialization

# API che mi torna i prezzi aggregati per fascia di prezzo e per livello scelto
@api_view(['GET'])
def lista_prezzi_medi(request):
    if request.method == 'GET':

        livello = request.GET.get('livello', None)
        if livello is not None:
            prezzi = DatiPrezzi.objects.exclude(prezzo=-1)\
            .values('stato', 'provincia', 'affitto_vendita', 'fascia_prezzo') \
            .annotate(num_annunci=Count('fascia_prezzo'), prezzo_medio=Avg('prezzo'))

            prezzi_serializer = PrezziMediSerializer(prezzi, many=True)
            prezzi = prezzi_serializer.data
            for prezzo in prezzi:
                nome_provincia = prezzo["provincia"]

                ## Svizzera
                if nome_provincia == "Moësa" \
                        or nome_provincia == "Circolo di Lugano est" \
                        or nome_provincia == "Circolo di Lugano ovest"\
                        or nome_provincia == "Lugano" \
                        or nome_provincia == "Arbedo-Castione" \
                        or nome_provincia == "Circolo dell'Isole" \
                        or nome_provincia == "Circolo di Locarno" \
                        or nome_provincia == "Mendrisio" \
                        or nome_provincia == "Circolo di Caneggio" \
                        or nome_provincia == "Circolo di Bellinzona" \
                        or nome_provincia == "Circolo d'Agno"\
                        or nome_provincia == "Gambarogno" \
                        or nome_provincia == "Monteceneri" \
                        or nome_provincia == "Circolo della Navegna"\
                        or nome_provincia == "Collina d'Oro"\
                        or nome_provincia == "Terre di Pedemonte"\
                        or nome_provincia == "Circolo di Vezia"\
                        or nome_provincia == "Circolo di Carona"\
                        or nome_provincia == "Circolo di Stabio"\
                        or nome_provincia == "Circolo della Magliasina"\
                        or nome_provincia == "Calanca"\
                        or nome_provincia == "Bellinzona"\
                        or nome_provincia == "Circolo di Balerna"\
                        or nome_provincia == "Circolo di Sessa"\
                        or nome_provincia == "Circolo della Riviera"\
                        or nome_provincia == "Soragno"\
                        or nome_provincia == "Circolo di Mendrisio"\
                        or nome_provincia == "Disentis/Mustér"\
                        or nome_provincia == "Sumvitg"\
                        or nome_provincia == "Faido":
                    prezzo["provincia"] = "Ticino"

                if nome_provincia == "Conthey" \
                        or nome_provincia == "Sierre" \
                        or nome_provincia == "Monthey" \
                        or nome_provincia == "Hérens"\
                        or nome_provincia == "Martigny"\
                        or nome_provincia == "Arosastrasse"\
                        or nome_provincia == "Visp"\
                        or nome_provincia == "Brig"\
                        or nome_provincia == "Bagnes"\
                        or nome_provincia == "Valais/Wallis"\
                        or nome_provincia == "Sion"\
                        or nome_provincia == "Route de la Télécabine"\
                        or nome_provincia == "Val-d'Illiez"\
                        or nome_provincia == "Nendaz"\
                        or nome_provincia == "Orsières"\
                        or nome_provincia == "Saint-Maurice"\
                        or nome_provincia == "Crans-Montana"\
                        or nome_provincia == "Anniviers"\
                        or nome_provincia == "Les Crosets"\
                        or nome_provincia == "Leuk"\
                        or nome_provincia == "Goms"\
                        or nome_provincia == "Mollens (VS)"\
                        or nome_provincia == "Westilich Ranon"\
                        or nome_provincia == "Leytron"\
                        or nome_provincia == "Grimisuat"\
                        or nome_provincia == "Kantonsstrasse"\
                        or nome_provincia == "Vex":
                    prezzo["provincia"] = "Vallese"

                if nome_provincia == "Albula" \
                        or nome_provincia == "Graubünden/Grigioni/Grischun" \
                        or nome_provincia == "Flims" \
                        or nome_provincia == "San Bastiaun"\
                        or nome_provincia == "Davos"\
                        or nome_provincia == "Prättigau/Davos"\
                        or nome_provincia == "Maloja"\
                        or nome_provincia == "Spinadascio"\
                        or nome_provincia == "Surselva"\
                        or nome_provincia == "Via Gunels" \
                        or nome_provincia == "Rofna"\
                        or nome_provincia == "Landquart"\
                        or nome_provincia == "Via dal Corvatsch"\
                        or nome_provincia == "Region Engiadina Bassa/Val Müstair"\
                        or nome_provincia == "Stradung"\
                        or nome_provincia == "Via del Corvatsh"\
                        or nome_provincia == "Viamala"\
                        or nome_provincia == "Vaz/Obervaz"\
                        or nome_provincia == "Plessur"\
                        or nome_provincia == "Cazis"\
                        or nome_provincia == "Imboden"\
                        or nome_provincia == "Bernina"\
                        or nome_provincia == "Surses"\
                        or nome_provincia == "Valsot"\
                        or nome_provincia == "Prättigauerstrasse"\
                        or nome_provincia == "Zernez"\
                        or nome_provincia == "Posta Veglia"\
                        or nome_provincia == "Tschiertschen-Praden":
                    prezzo["provincia"] = "Grigioni"

                ## Austria
                if nome_provincia == "Villach"\
                        or nome_provincia == "Klagenfurt-am-Worthersee":
                    prezzo["provincia"] = "Karnten"
                if nome_provincia == "Landeck":
                    prezzo["provincia"] = "Kitzbuhel"

                ## Slovenia
                if nome_provincia == "Kranj" \
                        or nome_provincia == "Skofja-Loka" \
                        or nome_provincia == "Trzic"\
                        or nome_provincia == "Jesenice"\
                        or nome_provincia == "Radovljica":
                    prezzo["provincia"] = "Gorenjska"

                if nome_provincia == "Tolmin"\
                        or nome_provincia == "Ajdovscina"\
                        or nome_provincia == "Nova-Gorica"\
                        or nome_provincia == "Idrija":
                    prezzo["provincia"] = "Primorska"

                if nome_provincia == "Piran"\
                        or nome_provincia == "Sezana"\
                        or nome_provincia == "Koper"\
                        or nome_provincia == "Izola":
                    prezzo["provincia"] = "Severna-Primorska"

                ## Francia
                if nome_provincia == "Route du Vieux Village":
                    prezzo["provincia"] = "Haute-Savoie"

                if nome_provincia == "Savoie - Copia":
                    prezzo["provincia"] = "Savoie"

            return JsonResponse(prezzi_serializer.data, safe=False)

# API che mi torna tutti la lista di prezzi presente nel DB
@api_view(['GET'])
def dettaglio_zona(request, zona):
    if request.method == 'GET':
        prezzi = DatiPrezzi.objects.exclude(prezzo=-1)

        livello = request.GET.get('livello', None)

        if livello is not None:
                if livello == "provincia":
                    if zona == "Ticino":
                        zona = ["Moësa", "Circolo di Lugano est", "Circolo di Lugano ovest", "Lugano", "Arbedo-Castione", "Circolo dell'Isole", "Circolo di Locarno", "Mendrisio", "Circolo di Caneggio", "Circolo di Bellinzona", "Circolo d'Agno", "Gambarogno", "Monteceneri", "Circolo della Navegna", "Collina d'Oro", "Terre di Pedemonte", "Circolo di Vezia", "Circolo di Carona", "Circolo di Stabio", "Circolo della Magliasina", "Calanca", "Bellinzona", "Circolo di Balerna", "Circolo di Sessa", "Circolo della Riviera", "Soragno", "Circolo di Mendrisio", "Disentis/Mustér", "Sumvitg", "Faido"]
                    elif zona == "Vallese":
                        zona = ["Conthey", "Sierre", "Monthey", "Hérens", "Martigny", "Arosastrasse", "Visp", "Brig", "Bagnes", "Valais/Wallis", "Sion", "Route de la Télécabine", "Val-d'Illiez", "Nendaz", "Orsières", "Saint-Maurice", "Crans-Montana", "Anniviers", "Les Crosets", "Leuk", "Goms", "Mollens (VS)", "Westilich Ranon", "Leytron", "Grimisuat", "Kantonsstrasse", "Vex"]
                    elif zona == "Grigioni":
                        zona = ["Albula", "Graubünden/Grigioni/Grischun", "Flims", "San Bastiaun", "Davos", "Prättigau/Davos", "Maloja", "Spinadascio", "Surselva", "Via Gunels" , "Rofna", "Landquart", "Via dal Corvatsch", "Region Engiadina Bassa/Val Müstair", "Stradung", "Via del Corvatsh", "Viamala", "Vaz/Obervaz", "Plessur", "Cazis", "Imboden", "Bernina", "Surses", "Valsot", "Prättigauerstrasse", "Zernez", "Posta Veglia", "Tschiertschen-Praden"]
                    elif zona == "Karnten":
                        zona = ["Villach", "Klagenfurt-am-Worthersee"]
                    elif zona == "Kitzbuhel":
                        zona = ["Landeck"]
                    elif zona == "Gorenjska":
                        zona = ["Kranj", "Skofja-Loka", "Trzic", "Jesenice", "Radovljica"]
                    elif zona == "Primorska":
                        zona = ["Tolmin", "Ajdovscina", "Nova-Gorica", "Idrija"]
                    elif zona == "Severna-Primorska":
                        zona = ["Piran", "Sezana", "Koper", "Izola"]
                    elif zona == "Haute-Savoie":
                        zona = ["Route du Vieux Village"]
                    else:
                        zona = [zona]
                    dati_zona = prezzi.filter(provincia__in=zona)
                else:
                    dati_zona = {}
        else:
            dati_zona = {}

        prezzi_serializer = PrezziSerializer(dati_zona, many=True)
        return JsonResponse(prezzi_serializer.data, safe=False)
        # 'safe=False' for objects serialization

# API che mi torna tutti la lista di zone vicine di ciascuna zona
@api_view(['GET'])
def vicini_zona(request, zona):
    if request.method == 'GET':

        livello = request.GET.get('livello', None)

        if livello is not None:
                if livello == "provincia":
                    vicini = [
                        ## Austria
                        {"zona": "Alpes-Maritimes", "vicini": ["Imperia", "Cuneo", "Alpes-de-Haute-Provence"]},
                        {"zona": "Alpes-de-Haute-Provence", "vicini": ["Hautes-Alpes", "Cuneo", "Alpes-Maritimes"]},
                        {"zona": "Hautes-Alpes", "vicini": ["Alpes-de-Haute-Provence", "Cuneo", "Torino", "Savoie"]},
                        {"zona": "Savoie", "vicini": ["Hautes-Alpes", "Aosta", "Torino", "Haute-Savoie"]},
                        {"zona": "Haute-Savoie", "vicini": ["Vallese", "Aosta", "Savoie"]},

                        ## Svizzera
                        {"zona": "Vallese", "vicini": ["Haute-Savoie", "Aosta", "Vercelli", "Verbania", "Ticino"]},
                        {"zona": "Ticino", "vicini": ["Vallese", "Sondrio", "Varese", "Verbania", "Grigioni", "Como"]},
                        {"zona": "Grigioni", "vicini": ["Como", "Sondrio", "Bolzano", "Solden", "Ticino"]},

                        ## Austria
                        {"zona": "Solden", "vicini": ["Innsbruck", "Bolzano", "Grigioni"]},
                        {"zona": "Innsbruck", "vicini": ["Solden", "Bolzano", "Kitzbuhel"]},
                        {"zona": "Kitzbuhel", "vicini": ["Zell-am-See", "Bolzano", "Innsbruck"]},
                        {"zona": "Zell-am-See", "vicini": ["Kitzbuhel", "Bolzano", "Lienz", "Spittal-An-Der-Drau"]},
                        {"zona": "Lienz", "vicini": ["Zell-am-See", "Bolzano", "Belluno", "Spittal-An-Der-Drau"]},
                        {"zona": "Spittal-An-Der-Drau", "vicini": ["Zell-am-See", "Udine", "Belluno", "Lienz", "Karnten"]},
                        {"zona": "Karnten", "vicini": ["Zell-am-See", "Udine", "Gorenjska", "Spittal-An-Der-Drau"]},

                        ## Slovenia
                        {"zona": "Gorenjska", "vicini": ["Karnten", "Udine", "Primorska"]},
                        {"zona": "Primorska", "vicini": ["Gorizia", "Udine", "Gorenjska", "Severna-Primorska"]},
                        {"zona": "Severna-Primorska", "vicini": ["Gorizia", "Trieste", "Primorska"]},

                        ## Italia
                        {"zona": "Trieste", "vicini": ["Gorizia", "Severna-Primorska"]},
                        {"zona": "Gorizia", "vicini": ["Severna-Primorska", "Trieste", "Primorska", "Udine"]},
                        {"zona": "Udine", "vicini": ["Karnten", "Gorenjska", "Primorska", "Gorizia", "Spittal-An-Der-Drau", "Belluno"]},
                        {"zona": "Belluno", "vicini": ["Spittal-An-Der-Drau", "Lienz", "Bolzano", "Udine"]},
                        {"zona": "Bolzano", "vicini": ["Belluno", "Lienz", "Zell-am-See", "Kitzbuhel", "Innsbruck", "Solden", "Grigioni", "Sondrio"]},
                        {"zona": "Sondrio", "vicini": ["Bolzano", "Grigioni", "Como"]},
                        {"zona": "Como", "vicini": ["Sondrio", "Grigioni", "Ticino", "Varese"]},
                        {"zona": "Varese", "vicini": ["Como", "Verbania", "Ticino"]},
                        {"zona": "Verbania", "vicini": ["Varese", "Ticino", "Vallese", "Vercelli"]},
                        {"zona": "Vercelli", "vicini": ["Verbania", "Vallese", "Aosta", "Torino"]},
                        {"zona": "Aosta", "vicini": ["Vercelli", "Vallese", "Haute-Savoie", "Savoie", "Torino"]},
                        {"zona": "Torino", "vicini": ["Aosta", "Vercelli", "Hautes-Alpes", "Savoie", "Cuneo"]},
                        {"zona": "Cuneo", "vicini": ["Torino", "Alpes-de-Haute-Provence", "Hautes-Alpes", "Alpes-Maritimes", "Imperia"]},
                        {"zona": "Imperia", "vicini": ["Cuneo", "Alpes-Maritimes"]},
                    ]
                    for vicini_container in vicini:
                        if vicini_container["zona"] == zona:
                            vicini_zona = {"vicini": vicini_container["vicini"]}
                else:
                    vicini_zona = {}
        else:
            vicini_zona = {}

    return JsonResponse(vicini_zona, safe=False)
    # 'safe=False' for objects serialization

# API che mi torna tutti la lista di prezzi presente nel DB
@api_view(['GET'])
def lista_flussi(request):
    if request.method == 'GET':
        livello = request.GET.get('livello', None)

        if livello is not None:
            if livello == "provincia":
                vicini = [
                    ## Austria
                    {"zona": "Alpes-Maritimes", "vicini": ["Imperia", "Cuneo"]},
                    {"zona": "Alpes-de-Haute-Provence", "vicini": [ "Cuneo"]},
                    {"zona": "Hautes-Alpes", "vicini": ["Cuneo", "Torino"]},
                    {"zona": "Savoie", "vicini": ["Aosta", "Torino"]},
                    {"zona": "Haute-Savoie", "vicini": ["Vallese", "Aosta",]},

                    ## Svizzera
                    {"zona": "Vallese", "vicini": ["Haute-Savoie", "Aosta", "Vercelli", "Verbania"]},
                    {"zona": "Ticino", "vicini": ["Sondrio", "Varese", "Verbania", "Como"]},
                    {"zona": "Grigioni", "vicini": ["Como", "Sondrio", "Bolzano", "Solden"]},

                    ## Austria
                    {"zona": "Solden", "vicini": ["Bolzano", "Grigioni"]},
                    {"zona": "Innsbruck", "vicini": ["Bolzano"]},
                    {"zona": "Kitzbuhel", "vicini": ["Bolzano"]},
                    {"zona": "Zell-am-See", "vicini": ["Bolzano"]},
                    {"zona": "Lienz", "vicini": ["Bolzano", "Belluno"]},
                    {"zona": "Spittal-An-Der-Drau", "vicini": ["Udine", "Belluno"]},
                    {"zona": "Karnten", "vicini": ["Udine", "Gorenjska"]},

                    ## Slovenia
                    {"zona": "Gorenjska", "vicini": ["Karnten", "Udine"]},
                    {"zona": "Primorska", "vicini": ["Gorizia", "Udine"]},
                    {"zona": "Severna-Primorska", "vicini": ["Gorizia", "Trieste"]},

                    ## Italia
                    {"zona": "Trieste", "vicini": ["Severna-Primorska"]},
                    {"zona": "Gorizia", "vicini": ["Severna-Primorska", "Primorska"]},
                    {"zona": "Udine", "vicini": ["Karnten", "Gorenjska", "Primorska", "Spittal-An-Der-Drau"]},
                    {"zona": "Belluno", "vicini": ["Spittal-An-Der-Drau", "Lienz"]},
                    {"zona": "Bolzano", "vicini": ["Lienz", "Zell-am-See", "Kitzbuhel", "Innsbruck", "Solden", "Grigioni"]},
                    {"zona": "Sondrio", "vicini": ["Grigioni"]},
                    {"zona": "Como", "vicini": ["Grigioni", "Ticino"]},
                    {"zona": "Varese", "vicini": ["Ticino"]},
                    {"zona": "Verbania", "vicini": ["Ticino", "Vallese"]},
                    {"zona": "Vercelli", "vicini": ["Vallese"]},
                    {"zona": "Aosta", "vicini": ["Vallese", "Haute-Savoie", "Savoie"]},
                    {"zona": "Torino", "vicini": ["Hautes-Alpes", "Savoie"]},
                    {"zona": "Cuneo", "vicini": ["Alpes-de-Haute-Provence", "Hautes-Alpes", "Alpes-Maritimes"]},
                    {"zona": "Imperia", "vicini": ["Alpes-Maritimes"]},
                ]
                mapping_latlong = [
                    {"Alpes-de-Haute-Provence": [44.164188, 6.232930]},
                    {"Alpes-Maritimes": [43.920700, 7.177140]},
                    {"Aosta": [45.735062, 7.313080]},
                    {"Belluno": [46.139900, 12.217670]},
                    {"Bolzano": [46.496720, 11.358000]},
                    {"Como": [45.808060, 9.085176]},
                    {"Cuneo": [44.384476, 7.542671]},
                    {"Gorenjska": [46.366692, 14.108510]},
                    {"Gorizia": [45.867670, 13.481890]},
                    {"Grigioni": [46.656030, 9.628640]},
                    {"Haute-Savoie": [46.052760, 6.432610]},
                    {"Hautes-Alpes": [44.656399, 6.248200]},
                    {"Imperia": [43.887901, 8.031570]},
                    {"Innsbruck": [47.262691, 11.394700]},
                    {"Karnten": [46.723969, 14.094810]},
                    {"Kitzbuhel": [47.445469, 12.391940]},
                    {"Lienz": [46.829460, 12.768950]},
                    {"Primorska": [46.002950, 14.027860]},
                    {"Savoie": [45.499149, 5.999980]},
                    {"Severna-Primorska": [45.596495, 14.044680]},
                    {"Solden": [46.966709, 11.007390]},
                    {"Sondrio": [46.171280, 9.869370]},
                    {"Spittal-An-Der-Drau": [46.798240, 13.495970]},
                    {"Ticino": [46.225101, 8.770980]},
                    {"Torino": [45.068371, 7.683070]},
                    {"Trieste": [45.653599, 13.778520]},
                    {"Udine": [46.064941, 13.230720]},
                    {"Vallese": [46.209260, 7.605560]},
                    {"Varese": [45.817631, 8.826380]},
                    {"Verbania": [45.921509, 8.551560]},
                    {"Vercelli": [45.321110, 8.426240]},
                    {"Zell-am-See": [47.323750, 12.796650]},
                ]
                for vicini_container in vicini:
                   for index, vicino in enumerate(vicini_container["vicini"]):
                       for coord in mapping_latlong:
                           if vicino in coord:
                               vicini_container["vicini"][index] = {"zona": vicino, "coord": coord[vicino]}
                           if vicini_container["zona"] in coord:
                               vicini_container["coord"] = coord[vicini_container["zona"]]
            else:
                vicini = {}
        else:
            vicini = {}
    return JsonResponse(vicini, safe=False)
    # 'safe=False' for objects serialization