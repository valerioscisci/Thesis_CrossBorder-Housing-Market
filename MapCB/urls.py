from django.urls import path
from MapCB.views.admin_views import upload_dati
from MapCB.views.remove_duplicates import rimuovi_duplicati
from MapCB.views.api import lista_prezzi

urlpatterns = [
    path('admin/admin_upload.html', upload_dati, name="upload_dati"),
    path('admin/rimuovi_duplicati', rimuovi_duplicati, name="rimuovi_duplicati"),
    path(r'^api/prezzi$', lista_prezzi),
]
