from pprint import pprint

from dadata import Dadata
from rest_framework.response import Response
from rest_framework.views import APIView

from api.lib import getDistance
from dadata_test.settings import DADATA_TOKEN, DADATA_SECRET
from main.models import City
from main.serializers import CityModelSerializer


class Address(APIView):
    def post(self, request):
        with Dadata(DADATA_TOKEN, DADATA_SECRET) as dadata:
            data = dadata.clean(name="address", source=request.data["address"])

        return Response({
            "status": "OK" if data["geo_lat"] and data['geo_lon'] else "error",
            "geo_lat": data["geo_lat"],
            "geo_lon": data['geo_lon']
        })


class RadiusFilter(APIView):
    def post(self, request):
        lan, lon, radius = float(request.data["lat"]), float(request.data["lon"]), float(request.data["radius"])

        return Response([CityModelSerializer(city).data for city in City.objects.all()
                         if getDistance(lan, lon, city.geo_lat, city.geo_lon) < radius])
