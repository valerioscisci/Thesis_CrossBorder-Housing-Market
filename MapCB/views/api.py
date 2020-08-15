# Django Imports
from django.db.models import Count
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
            .values('provincia', 'affitto_vendita', 'fascia_prezzo') \
            .annotate(num_annunci=Count('fascia_prezzo'))

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
