from django.db import models


class Country(models.Model):
    name = models.CharField("Название", max_length=1024)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = verbose_name_plural = "Страна"


class FederalDistrict(models.Model):
    federal_district = models.CharField("Название", max_length=1024)
    country = models.ForeignKey(Country, models.CASCADE, "federal_districts", verbose_name="Страна")

    def __str__(self):
        return f"{self.federal_district} ({self.country.name})"

    class Meta:
        verbose_name = verbose_name_plural = "Федеральный округ"


class RegionType(models.Model):
    name = models.CharField("Название", max_length=1024)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = verbose_name_plural = "Тип региона"


class Region(models.Model):
    region = models.CharField("Название", max_length=1024)
    region_type = models.ForeignKey(RegionType, models.CASCADE, "regions", verbose_name="Страна")
    federal_district = models.ForeignKey(FederalDistrict, models.CASCADE, "regions", verbose_name="Страна")

    def __str__(self):
        return f"{self.region} ({self.federal_district})"

    class Meta:
        verbose_name = verbose_name_plural = "Регион"


class AreaType(models.Model):
    name = models.CharField("Название", max_length=1024)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = verbose_name_plural = "Тип района"


class Area(models.Model):
    area = models.CharField("Название", max_length=1024)
    area_type = models.ForeignKey(AreaType, models.CASCADE, "areas", verbose_name="Тип района")

    def __str__(self):
        return f"{self.area}"

    class Meta:
        verbose_name = verbose_name_plural = "Район"


class CityType(models.Model):
    name = models.CharField("Название", max_length=1024)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = verbose_name_plural = "Тип города"


class FiasLevel(models.Model):
    name = models.IntegerField("Название")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = verbose_name_plural = "Уровень ФИАС"


class TaxOffice(models.Model):
    name = models.CharField("Название", max_length=1024)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = verbose_name_plural = "Налоговый офис"


class CapitalMarker(models.Model):
    name = models.CharField("Название", max_length=1024)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = verbose_name_plural = "Маркер столицы"


class City(models.Model):
    city = models.CharField("Название", max_length=1024, null=True, blank=True)
    city_type = models.ForeignKey(CityType, models.CASCADE, "cities", verbose_name="Тип города", null=True, blank=True)
    address = models.CharField("Адрес", max_length=1024)
    postal_code = models.CharField("Почтовый код", max_length=36, null=True, blank=True)
    region = models.ForeignKey(Region, models.CASCADE, "cities", verbose_name="Регион")
    area = models.ForeignKey(Area, models.CASCADE, "cities", verbose_name="Район", null=True, blank=True)
    kladr_id = models.IntegerField("КЛАДР")
    fias_id = models.CharField("ФИАС", max_length=36)
    fias_level = models.ForeignKey(FiasLevel, models.CASCADE, "cities", verbose_name="Уровень ФИАС")
    capital_marker = models.ForeignKey(CapitalMarker, models.CASCADE, "cities", verbose_name="Маркер столицы")
    okato = models.CharField("ОКАТО", max_length=36, null=True, blank=True)
    oktmo = models.CharField("ОКТМО", max_length=36, null=True, blank=True)
    tax_office = models.ForeignKey(TaxOffice, models.CASCADE, "cities", verbose_name="Налоговая", null=True, blank=True)
    timezone = models.CharField("Временная зона", max_length=8, null=True, blank=True)
    geo_lat = models.FloatField("Широта")
    geo_lon = models.FloatField("Долгота")
    population = models.CharField("Население", max_length=36)
    foundation_year = models.CharField("Основан", max_length=1024, null=True, blank=True)
    settlement = models.CharField("Посёлок", max_length=1024, null=True, blank=True)
    settlement_type = models.ForeignKey(CityType, models.CASCADE, "settlements", verbose_name="Тип посёлка",
                                        null=True, blank=True)

    @property
    def federal_district(self):
        return self.region.federal_district

    @property
    def country(self):
        return self.region.federal_district.country

    @property
    def region_type(self):
        return self.region.region_type

    @property
    def area_type(self):
        return self.area.area_type

    def __str__(self):
        base_name = ""
        if self.city and not self.settlement:
            base_name = self.city
        elif not self.city and self.settlement:
            base_name = self.settlement
        elif self.city and self.settlement:
            base_name = f"{self.settlement} ({self.city})"
        elif not self.city and not self.settlement:
            base_name = f"{self.region.region}"

        return f"{base_name}"

    class Meta:
        verbose_name = verbose_name_plural = "Город"
