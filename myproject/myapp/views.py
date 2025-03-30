from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("А теперь надо выбрать admin?api?swagger итд)")

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer