from rest_framework.response import Response
from rest_framework.views import APIView

from api.lib import getDistance
from api.serializers import DadataSerializer, RadiusFilterSerializer
from dadata_test.settings import DADATA
from main.models import City
from main.serializers import CityModelSerializer


class Address(APIView):
    def post(self, request):
        return Response(DadataSerializer(DADATA.clean(name="address", source=request.data["address"])).data)


class RadiusFilter(APIView):
    def post(self, request):
        radius_serializer = RadiusFilterSerializer(data=request.data)
        if radius_serializer.is_valid():
            data = radius_serializer.validated_data
            return Response([CityModelSerializer(city).data for city in City.objects.all()
                             if getDistance(data["lat"], data["lon"], city.geo_lat, city.geo_lon) < data["radius"]])
