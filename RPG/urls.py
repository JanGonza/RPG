from django.urls import path
from . import views

app_name = 'RPG'
urlpatterns = [
    path('', views.content, name='content'),
    path('<int:page_number>', views.content, name='content'),
]