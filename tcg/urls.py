from tcg.views import *
from django.urls import path, include

from . import views
urlpatterns = [
    path('', views.all_cards, name='all_cards'),
    path('vault', views.vault, name='vault'),
    path('trade_select', views.trade_select, name="trade_select"),
    path('trade/offers/create_offer',views.CreateOffer.as_view(), name="trade_offer"),
    path('trade/offers', views.MyOffers.as_view(), name="myoffers"),
    path('trade/offers/<int:pk>', views.OfferDetailView.as_view(), name="offer"),
    path('trade/', views.MyTrades.as_view(), name="mytrades"),
    path('trade/<int:pk>', views.TradeDetailView.as_view(), name="trade"),
    path('trade/offers/counter_offer/<int:trade_pk>', views.CreateCounterOffer.as_view(), name="counter_offer"),
    path('market', views.Market.as_view(), name="market"),
]

