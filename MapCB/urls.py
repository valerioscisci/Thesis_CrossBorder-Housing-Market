# Django Imports
from django.urls import path
from django.contrib.auth import views as auth_views

# Other Imports
from MapCB.views.admin_views import upload_dati
from MapCB.views.api import lista_prezzi
from MapCB.views.static_views import HomepageView

# Url generali sito

urlpatterns = [
    path('', HomepageView.as_view(), name='home'),  #  Homepage
]


# Url sezione admin

urlpatterns += [
    path('admin/admin_upload.html', upload_dati, name="upload_dati"),
]

# Url API

urlpatterns += [
    path(r'api/prezzi', lista_prezzi),
]

# Login + Password Change
urlpatterns += [
    path('login/', auth_views.LoginView, {'template_name': 'registration/login.html'}, name='login'),  #Login
    path('logout/', auth_views.LoginView, {'next_page': '/'}, name='logout'),  #Logout
    path('password_change/', auth_views.PasswordChangeView, {'template_name': 'registration/password_change.html'} , name='password_change'),  #Password Change
    path('password-change-done/', auth_views.PasswordChangeDoneView, {'template_name': 'registration/password_change_done.html'}, name='password_change_done'),  #Password Change
]