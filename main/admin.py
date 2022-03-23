from django.contrib import admin
from main.models import City, CapitalMarker, FiasLevel, Region, RegionType, FederalDistrict, Country, TaxOffice, \
    CityType, AreaType, Area

for model in [City, CapitalMarker, FiasLevel, Region, RegionType, FederalDistrict, Country, TaxOffice, CityType,
              AreaType, Area]:
    admin.site.register(model)
