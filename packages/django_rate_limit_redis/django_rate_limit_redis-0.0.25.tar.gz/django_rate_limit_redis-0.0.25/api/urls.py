from django_rate_limit_redis.decorators import rate_limit
from rest_framework.routers import DefaultRouter

from django.urls import include
from django.urls import path

from . import views

router = DefaultRouter()

router.register(r'stores', views.StoreViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('sku/<str:EAN13>/residues/', rate_limit(system='api')(views.ResidueView.as_view()), name='residue-list'),
    path('bonuses/payments/', rate_limit(system='api')(views.BonusPaymentView.as_view()), name='bonus_payment-list'),
]
