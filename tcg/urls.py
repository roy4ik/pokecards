from django.urls import path, include

from . import views
urlpatterns = [
    path('', views.all_cards, name='all_cards'),
]

