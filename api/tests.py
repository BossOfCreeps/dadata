from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from main.models import City, FiasLevel, CapitalMarker, Region, RegionType, FederalDistrict, Country


class AddressTestCase(TestCase):
    def test_address_success(self):
        with patch('dadata.Dadata.clean', return_value={'geo_lat': 1.1, 'geo_lon': 2.23}):
            resp = self.client.post(reverse('Address'), {'address': 'москва 3 улица строителей дом 25'}, format='json')
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            self.assertEqual(resp.data, {'status': 'OK', 'geo_lat': 1.1, 'geo_lon': 2.23})

    def test_address_error_no_address(self):
        with patch('dadata.Dadata.clean', return_value={'geo_lat': None, 'geo_lon': None}):
            resp = self.client.post(reverse('Address'), {'address': 'нью йорк'}, format='json')
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            self.assertEqual(resp.data, {'status': 'error', 'geo_lat': None, 'geo_lon': None})


class RadiusFilterTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        for i, el in enumerate([[50, 80], [54, 85], [50, 100], [70, 80], [45, 75], [51, 79]]):
            City.objects.create(
                address=f"Адрес {i}",
                region=Region.objects.get_or_create(
                    name=f"Название {i}",
                    region_type=RegionType.objects.get_or_create(name="Тип региона")[0],
                    federal_district=FederalDistrict.objects.get_or_create(
                        name="Федеральный округ",
                        country=Country.objects.get_or_create(name="Страна")[0]
                    )[0]
                )[0],
                kladr_id="123",
                fias_id="456",
                fias_level=FiasLevel.objects.get_or_create(name=1)[0],
                capital_marker=CapitalMarker.objects.get_or_create(name=1)[0],
                geo_lat=el[0],
                geo_lon=el[1],
                population=1000
            )

    @classmethod
    def tearDownClass(cls):
        City.objects.all().delete()

    def test_radius_part(self):
        resp = self.client.post(reverse('RadiusFilter'), {'lat': 50, 'lon': 80, 'radius': 1000}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, [{'__str__': 'Название 0', 'geo_lon': 80.0, 'geo_lat': 50.0},
                                     {'__str__': 'Название 1', 'geo_lon': 85.0, 'geo_lat': 54.0},
                                     {'__str__': 'Название 4', 'geo_lon': 75.0, 'geo_lat': 45.0},
                                     {'__str__': 'Название 5', 'geo_lon': 79.0, 'geo_lat': 51.0}])

    def test_radius_empty_bad_lat_lon(self):
        resp = self.client.post(reverse('RadiusFilter'), {'lat': 10, 'lon': 10, 'radius': 1000}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, [])

    def test_radius_empty_small_radius(self):
        resp = self.client.post(reverse('RadiusFilter'), {'lat': 51, 'lon': 81, 'radius': 10}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, [])

    def test_radius_all(self):
        resp = self.client.post(reverse('RadiusFilter'), {'lat': 51, 'lon': 81, 'radius': 40000}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, [{'__str__': 'Название 0', 'geo_lon': 80.0, 'geo_lat': 50.0},
                                     {'__str__': 'Название 1', 'geo_lon': 85.0, 'geo_lat': 54.0},
                                     {'__str__': 'Название 2', 'geo_lon': 100.0, 'geo_lat': 50.0},
                                     {'__str__': 'Название 3', 'geo_lon': 80.0, 'geo_lat': 70.0},
                                     {'__str__': 'Название 4', 'geo_lon': 75.0, 'geo_lat': 45.0},
                                     {'__str__': 'Название 5', 'geo_lon': 79.0, 'geo_lat': 51.0}])
