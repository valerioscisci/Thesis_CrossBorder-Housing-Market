from django.db.models import Count, Max
from django.http import JsonResponse

from MapCB.models import DatiPrezzi

def rimuovi_duplicati(request):
    unique_fields = ['stato', 'regione', 'provincia', 'comune', 'indirizzo', 'metri_quadri', 'prezzo']

    duplicates = (
         DatiPrezzi.objects.values())#values(*unique_fields)
    #     .order_by()
    #     .annotate(max_id=Max('id'), count_id=Count('id'))
    #     .filter(count_id__gt=1)
    # )
    print(list(duplicates))
    for duplicate in duplicates:
        (
            DatiPrezzi.objects
            .filter(**{x: duplicate[x] for x in unique_fields})
            .exclude(id=duplicate['max_id'])
            .delete()
        )
    return JsonResponse(list(duplicates), safe=False)