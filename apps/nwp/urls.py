from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.lobby),
    path('nwp-api/',csrf_exempt(views.nwp)),
    # path('saveselection', csrf_exempt(views.saveselection))
]