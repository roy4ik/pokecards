from tcg.views import Create_offer
from django.urls import path, include

from . import views
urlpatterns = [
    path('', views.all_cards, name='all_cards'),
    path('vault', views.vault, name='vault'),
    path('trade_select', views.trade_select, name="trade_select"),
    path('create_offer',views.Create_offer.as_view(), name="trade_offer_made"),
    path('offer/<int:pk>', views.Tade)
    path('offer/<int:pk>/counter_offer', views.Counter_offer_Form, name="counter_offer")
]

