from rest_framework import serializers


class DadataSerializer(serializers.Serializer):
    status = serializers.SerializerMethodField()
    geo_lat = serializers.FloatField()
    geo_lon = serializers.FloatField()

    @staticmethod
    def get_status(obj) -> str:
        return "OK" if obj["geo_lat"] and obj["geo_lon"] else "error"


class RadiusFilterSerializer(serializers.Serializer):
    radius = serializers.FloatField()
    lat = serializers.FloatField()
    lon = serializers.FloatField()
