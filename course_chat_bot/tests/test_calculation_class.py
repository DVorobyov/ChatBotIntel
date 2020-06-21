import unittest
from unittest import mock
from course_chat_bot.calculation_class import Calculations
import requests
import mongomock
import pymongo
from course_chat_bot.sources.Calc_src.Corona_src import CoronaBdWork


class TestCalculationClass(unittest.TestCase):

    def setUp(self):
        pymongo.MongoClient = mongomock.MongoClient

    def test_get_msg_for_corona(self):
        CoronaBdWork.get_sorted_corona_list = mock.MagicMock(
            return_value=[{'FIPS': '', 'Admin2': '', 'Province_State': '',
                           'Country_Region': 'Spain',
                           'Last_Update': '2020-05-04 02:32:28',
                           'Lat': '40.463667', 'Long_': '-3.74922',
                           'Confirmed': 217466,
                           'Deaths': 25264, 'Recovered': 118902,
                           'Active': 73300,
                           'Combined_Key': 'Spain'}]
            )
        self.assertEqual(type(Calculations.get_msg_for_corona(
            'message for testing 03:05:2020')), str)

    def test_corona_stats_dynamics_1(self):
        self.assertIsInstance(Calculations.corona_stats_dynamics(
            'message for testing 03:05:2020'), str)

    def test_corona_stats_dynamics_2(self):
        self.assertTrue(int(Calculations.corona_stats_dynamics(
            'message for testing 03:05:2020').
                            split(' ')[3]) > 0)

    def test_get_position_weather_1(self):
        self.assertIsInstance(Calculations.get_position_weather(), dict)

    @mock.patch.object(requests, 'get', return_value=requests.get(
        'https://yandex.ru/pogoda/not_url_actually'))
    def test_get_position_weather_2(self, mocked_get):
        self.assertIsNone(Calculations.get_position_weather())

    def test_get_position_weather_3(self):
        self.assertTrue(Calculations.get_position_weather()['position'] >= 0)

    def test_get_weather(self):
        self.assertIsInstance(Calculations.get_weather(), str)

    def test_get_cat_fact_1(self):
        client = pymongo.MongoClient()
        cat_facts = client.mongo_bd.cat_facts
        cat_facts.drop()
        self.assertIsInstance(Calculations.get_cat_fact(), str)

    @mock.patch.object(requests, 'get', return_value=requests.get(
        'https://yandex.ru/pogoda/not_url_actually'))
    def test_get_cat_fact_2(self, mocked_get):
        self.assertIsInstance(Calculations.get_cat_fact(), str)

    def test_horoscope(self):
        self.assertIn('.', Calculations.get_horoscope('/horo овен'))

if __name__ == '__main__':
    unittest.main()
