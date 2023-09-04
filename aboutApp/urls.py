from django.urls import path
from . import views

app_name = 'aboutApp'

urlpatterns = [
    path('survey/', views.survey, name='survey'),
    path('contact/', views.contact, name='contact'),
    path('idea/', views.idea, name='idea'),
    path('limit/',views.stores,name='limit'),
    path('storeDetail/<int:id>/', views.storeDetail, name='storeDetail'),

]
