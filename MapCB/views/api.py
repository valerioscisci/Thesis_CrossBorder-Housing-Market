# Django Imports
from django.http.response import JsonResponse
from rest_framework.decorators import api_view

# Other Imports
from MapCB.serializers import PrezziSerializer
from MapCB.models import DatiPrezzi

@api_view(['GET', 'POST', 'DELETE'])
def lista_prezzi(request):
    if request.method == 'GET':
        prezzi = DatiPrezzi.objects.all()

        prezzi_serializer = PrezziSerializer(prezzi, many=True)
        return JsonResponse(prezzi_serializer.data, safe=False)
        # 'safe=False' for objects serialization
