from django.urls import path
from MapCB.views.admin_views import upload_dati

urlpatterns = [
    path('admin/admin_upload.html', upload_dati, name="upload_dati"),
]
