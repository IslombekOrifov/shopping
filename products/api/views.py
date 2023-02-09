from rest_framework import generics

from ..models import Brand

from .serializers import BrandSerializer


class BrandListView(generics.ListAPIView):
    queryset = Brand.objects.filter(active=True)
    serializer_class = BrandSerializer

