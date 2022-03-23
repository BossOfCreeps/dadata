from rest_framework import serializers

from main.models import City, CapitalMarker, FiasLevel, Region, RegionType, FederalDistrict, Country, TaxOffice, \
    CityType, AreaType, Area


class FederalDistrictSerializer(serializers.Serializer):
    federal_district = serializers.CharField()
    country = serializers.CharField()

    def create(self, validated_data):
        validated_data["country"] = Country.objects.get_or_create(name=validated_data["country"])[0]
        return FederalDistrict.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass


class AreaSerializer(serializers.Serializer):
    area = serializers.CharField()
    area_type = serializers.CharField()

    def create(self, validated_data):
        validated_data["area_type"] = AreaType.objects.get_or_create(name=validated_data["area_type"])[0]
        return Area.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass


class RegionSerializer(serializers.Serializer):
    region = serializers.CharField()
    region_type = serializers.CharField()
    country = serializers.CharField()
    federal_district = serializers.CharField()

    def create(self, validated_data):
        validated_data["region_type"] = RegionType.objects.get_or_create(name=validated_data["region_type"])[0]

        federal_district_serializer = FederalDistrictSerializer(data=validated_data)
        if federal_district_serializer.is_valid():
            validated_data["federal_district"] = federal_district_serializer.save()

        del validated_data["country"]

        return Region.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass


class CitySerializer(serializers.Serializer):
    city = serializers.CharField(allow_blank=True, allow_null=True)
    address = serializers.CharField()
    postal_code = serializers.CharField(allow_blank=True, allow_null=True)
    kladr_id = serializers.IntegerField()
    fias_id = serializers.CharField()
    okato = serializers.CharField(allow_blank=True, allow_null=True)
    oktmo = serializers.CharField(allow_blank=True, allow_null=True)
    timezone = serializers.CharField(allow_blank=True, allow_null=True)
    geo_lat = serializers.FloatField()
    geo_lon = serializers.FloatField()
    population = serializers.CharField()
    foundation_year = serializers.CharField(allow_blank=True, allow_null=True)
    settlement = serializers.CharField(allow_blank=True, allow_null=True)
    # For ForeignKey key
    capital_marker = serializers.CharField()
    fias_level = serializers.IntegerField()
    region = serializers.CharField()
    tax_office = serializers.CharField(allow_blank=True, allow_null=True)
    city_type = serializers.CharField(allow_blank=True, allow_null=True)
    area = serializers.CharField(allow_blank=True, allow_null=True)
    settlement_type = serializers.CharField(allow_blank=True, allow_null=True)
    # For ForeignKey additional data
    region_type = serializers.CharField()
    federal_district = serializers.CharField()
    country = serializers.CharField()
    area_type = serializers.CharField(allow_blank=True, allow_null=True)

    def create(self, validated_data):
        validated_data["capital_marker"] = CapitalMarker.objects.get_or_create(name=validated_data["capital_marker"])[0]
        validated_data["fias_level"] = FiasLevel.objects.get_or_create(name=validated_data["fias_level"])[0]
        validated_data["tax_office"] = TaxOffice.objects.get_or_create(name=validated_data["tax_office"])[0]

        if validated_data["city_type"]:
            validated_data["city_type"] = CityType.objects.get_or_create(name=validated_data["city_type"])[0]
        else:
            validated_data["city_type"] = None

        region_serializer = RegionSerializer(data=validated_data)
        if region_serializer.is_valid():
            validated_data["region"] = region_serializer.save()

        if validated_data["area"]:
            area_serializer = AreaSerializer(data=validated_data)
            if area_serializer.is_valid():
                validated_data["area"] = area_serializer.save()
        else:
            validated_data["area"] = None

        if validated_data["settlement_type"]:
            validated_data["settlement_type"] = \
                CityType.objects.get_or_create(name=validated_data["settlement_type"])[0]
        else:
            validated_data["settlement_type"] = None

        for key in ["region_type", "federal_district", "country", "area_type"]:
            del validated_data[key]

        return City.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass


class CityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['__str__', 'geo_lon', 'geo_lat']
