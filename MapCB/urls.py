from django.urls import path
from MapCB.views.admin_views import upload_dati
from MapCB.views.api import lista_prezzi

urlpatterns = [
    path('admin/admin_upload.html', upload_dati, name="upload_dati"),
    path(r'api/prezzi', lista_prezzi),
]
