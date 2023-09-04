from django.urls import path
from . import views

app_name='productsApp'

urlpatterns=[
    path('survey/',views.survey,name='survey'),
    path('honor/',views.honor,name='honor'),
    path('melody/',views.melody,name='melody'),
    path('getDoc/<int:id>/', views.getDoc, name='getDoc'),

    path('download/', views.download, name='download'),  # 资料下载
]
