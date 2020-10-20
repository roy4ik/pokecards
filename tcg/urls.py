from django.urls import path, include

from . import views
urlpatterns = [
    path('', views.all_cards, name='all_cards'),
    path('vault_new', views.vault_new, name='vault_new'),
]

