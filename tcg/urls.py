from tcg.views import *
from django.urls import path, include

from . import views
urlpatterns = [
    path('', views.all_cards, name='all_cards'),
    path('vault', views.vault, name='vault'),
    path('trade_select', views.trade_select, name="trade_select"),
    path('create_offer',views.CreateOffer.as_view(), name="trade_offer_made"),
    # path('trade/<int:pk>', views.Trade.as_view(), name="trade"),
    path('trade/<int:pk>/counter_offer', views.CreateCounterOffer.as_view(), name="counter_offer")
]

