from rate_limit.decorators import rate_limit
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django.utils.decorators import method_decorator

from core.models import BonusPayment
from core.models import Order
from core.models import Residue
from core.models import Store
from .serializers import BonusSerializer
from .serializers import OrderSerializer
from .serializers import ResidueSerializer
from .serializers import StoreSerializer


class AuthViewMixin(object):
    permission_classes = (IsAuthenticated,)


@method_decorator(rate_limit(system='api'), name='list')
class StoreViewSet(viewsets.ReadOnlyModelViewSet, AuthViewMixin):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    lookup_field = 'pos_ext_id'
    pagination_class = None


@method_decorator(rate_limit(system='api'), name='list')
class ResidueView(generics.ListAPIView, AuthViewMixin):
    queryset = Residue.objects.get_queryset().order_by('-created_at')
    serializer_class = ResidueSerializer
    lookup_field = 'ean13'
    lookup_url_kwarg = 'ean13'


@method_decorator(rate_limit(system='api'), name='list')
class OrderViewSet(viewsets.ReadOnlyModelViewSet, AuthViewMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'order_id'
    pagination_class = None


@method_decorator(rate_limit(system='api'), name='list')
class BonusPaymentView(generics.ListAPIView, AuthViewMixin):
    queryset = BonusPayment.objects.all().order_by('-id')
    serializer_class = BonusSerializer
