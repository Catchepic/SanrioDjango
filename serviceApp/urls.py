from django.urls import path
from . import views

app_name='serviceApp'

urlpatterns=[
    path('globalSanrio/',views.globalSanrio,name='globalSanrio'),
]
