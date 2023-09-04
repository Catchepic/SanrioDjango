from django.urls import path
from . import views

app_name='contactApp'

urlpatterns=[
    path('recruit/', views.recruit, name='recruit'),  # 加入恒达
]
