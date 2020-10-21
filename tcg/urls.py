from django.urls import path, include

from . import views
urlpatterns = [
    path('', views.all_cards, name='all_cards'),
    path('vault', views.vault, name='vault'),
    path('trade_select', views.trade_select, name="trade_select")
]

