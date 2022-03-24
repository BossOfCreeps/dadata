import csv
import filecmp
import os
import shutil
from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from django.test import TestCase
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException

from main.models import City
from main.serializers import CityCsvModelSerializer


def replace_none(test_dict):
    if isinstance(test_dict, dict):
        for key in test_dict:
            if test_dict[key] is None:
                test_dict[key] = ''
            else:
                replace_none(test_dict[key])

    elif isinstance(test_dict, list):
        for val in test_dict:
            replace_none(val)


class CommandsTestCase(TestCase):
    def tearDown(self):
        City.objects.all().delete()

    def test_command_parse_to_db(self):
        test_csv_path = "city.csv"  # test_data/test_
        call_command("parse_to_db", test_csv_path, verbosity=0)

        right = [row for row in csv.DictReader(open(test_csv_path, encoding='utf-8'))]
        result = [CityCsvModelSerializer(city).data for city in City.objects.all()]
        replace_none(result)
        right.sort(key=lambda x: x['address'], reverse=False)
        result.sort(key=lambda x: x['address'], reverse=False)
        self.assertEqual(result, right)


class SeleniumTests(StaticLiveServerTestCase):
    selenium = None
    test_folder = os.path.join("test_data", "test")
    right_folder = os.path.join("test_data", "right")
    delay = 3

    @classmethod
    def setUpClass(cls):
        cls.selenium = webdriver.Chrome("chromedriver.exe")
        cls.selenium.implicitly_wait(10)
        cls.selenium.get("http://127.0.0.1:8000")
        cls.selenium.set_window_size(1500, 1200)

        if os.path.exists(cls.test_folder):
            shutil.rmtree(cls.test_folder)
        os.mkdir(cls.test_folder)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        City.objects.all().delete()
        if os.path.exists(cls.test_folder):
            shutil.rmtree(cls.test_folder)

    def setUp(self):
        self.selenium.refresh()

    def test_empty(self):
        name = "empty.png"
        sleep(self.delay)
        self.selenium.save_screenshot(os.path.join(self.test_folder, name))
        self.assertTrue(filecmp.cmp(os.path.join(self.test_folder, name), os.path.join(self.right_folder, name)))

    def test_address_success(self):
        name = "address.png"
        self.selenium.find_element_by_id("address_input").send_keys('томск ленина 30')
        self.selenium.find_element_by_id("address_submit").click()
        sleep(self.delay)
        self.selenium.save_screenshot(os.path.join(self.test_folder, name))
        self.assertTrue(filecmp.cmp(os.path.join(self.test_folder, name), os.path.join(self.right_folder, name)))

    def test_address_error(self):
        with self.assertRaises(UnexpectedAlertPresentException):
            self.selenium.find_element_by_id("address_input").send_keys('лондон')
            self.selenium.find_element_by_id("address_submit").click()
            sleep(self.delay)
            self.selenium.save_screenshot("1.png")

    def test_radius_part(self):
        name = "radius.png"
        self.selenium.find_element_by_id("radius_lat_input").send_keys('50')
        self.selenium.find_element_by_id("radius_lon_input").send_keys('80')
        self.selenium.find_element_by_id("radius_input").send_keys('1000')
        self.selenium.find_element_by_id("radius_submit").click()
        sleep(self.delay)
        self.selenium.save_screenshot(os.path.join(self.test_folder, name))
        self.assertTrue(filecmp.cmp(os.path.join(self.test_folder, name), os.path.join(self.right_folder, name)))

    def test_radius_empty_bad_lat_lon(self):
        with self.assertRaises(UnexpectedAlertPresentException):
            self.selenium.find_element_by_id("radius_lat_input").send_keys('0')
            self.selenium.find_element_by_id("radius_lon_input").send_keys('0')
            self.selenium.find_element_by_id("radius_input").send_keys('1000')
            self.selenium.find_element_by_id("radius_submit").click()
            sleep(self.delay)
            self.selenium.save_screenshot("1.png")

    def test_radius_empty_small_radius(self):
        with self.assertRaises(UnexpectedAlertPresentException):
            self.selenium.find_element_by_id("radius_lat_input").send_keys('50')
            self.selenium.find_element_by_id("radius_lon_input").send_keys('80')
            self.selenium.find_element_by_id("radius_input").send_keys('100')
            self.selenium.find_element_by_id("radius_submit").click()
            sleep(self.delay)
            self.selenium.save_screenshot("1.png")
