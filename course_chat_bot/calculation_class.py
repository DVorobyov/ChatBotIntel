import requests
import pymongo
import datetime
from random import random
from sources.Calc_src.Corona_src import CoronaBdWork
from sources.Calc_src.Horoscope \
    import horo_message_parse, get_horoscope_str


class Calculations:

    @staticmethod
    def print_poem(message: str):  # str
        client = pymongo.MongoClient()
        bd = client.mongo_bd
        collection = bd.poems
        result = ''
        for line in collection.find():
            if line["text"].find(message) > -1:
                result = line["text"]
        if result == '':
            result = 'Not found :('
        return result

    @staticmethod
    def get_msg_for_corona(message: str):    # str
        try:
            sort_dictlist = CoronaBdWork(pymongo.MongoClient())\
                .get_sorted_corona_list(CoronaBdWork.message_parse(message))
        except BaseException:
            return 'Error occurred'
        msg = f'Топ 5 местностей по зарегистрированным заражениям на ' \
            f'{str(CoronaBdWork.message_parse(message))}:\n'
        for i in range(0, 5):
            if i >= len(sort_dictlist):
                break
            if len((sort_dictlist[i]['Province_State'])) > 0:
                msg += sort_dictlist[i]['Province_State'] + ':'
            msg += sort_dictlist[i]['Country_Region'] + '\n'
        return msg

    @staticmethod
    def corona_stats_dynamics(message: str):
        return f"За {str(CoronaBdWork.message_parse(message) - datetime.timedelta(days=1))}" \
                   f" заразилось " + \
                   str(CoronaBdWork(pymongo.MongoClient()).
                       today_yesterday_diff(
                       CoronaBdWork.message_parse(message))) + " человек"

    @staticmethod
    def get_weather():  # str
        # TODO: запихать вычисления погоды в sources
        message = ''
        try:
            resp = Calculations.get_position_weather()
            html_weather = resp['html_text']
            position = resp['position']
        except BaseException:
            return 'Error occurred'
        temperature = ''
        counter = 0
        while html_weather[position + counter] != "<":
            temperature += html_weather[position + counter]
            counter += 1
        position = html_weather.find('<div class="link__condition'
                                     ' day-anchor i-bem" data-bem=') + len(
            '<div class="link__condition day-anchor i-bem" data-bem=')
        fl = False
        condition = ''
        counter = 0
        while html_weather[position + counter] != "<":
            if fl:
                condition += html_weather[position + counter]
            if html_weather[position + counter] == ">":
                fl = True
            counter += 1
        message += 'Температура: ' + temperature + "\n" + condition
        return message

    @staticmethod
    def get_position_weather():
        req = requests.get(
            'https://yandex.ru/pogoda/47?utm_source'
            '=serp&utm_campaign'
            '=wizard&utm_medium=desktop&utm_content='
            'wizard_desktop_main&utm_term=title')
        if req.status_code != 200:
            return None
        html_weather = req.text
        position = html_weather.rfind(
            '<div class="temp fact__temp fact__temp_size_s" role="text">'
            '<span class="temp__pre-a11y a11y-hidden">'
            'Текущая температура</span><span class="temp__value">') + len(
            '<div class="temp fact__temp fact__temp_size_s" role="text">'
            '<span class="temp__pre-a11y a11y-hidden">'
            'Текущая температура</span><span class="temp__value">')
        if position < 0:
            return None
        else:
            return {'html_text': html_weather, 'position': position}

    @staticmethod
    def get_cat_fact():
        # TODO: запихать работу с базой и фактами тоже в sources
        #  и там написать на них тесты
        try:
            msg = Calculations.fact_selection(pymongo.MongoClient().mongo_bd)
        except BaseException:
            return "Error occurred"
        return f'Fact: \n{msg}'

    @staticmethod
    def fact_selection(bd):
        if 'cat_facts' not in bd.list_collection_names():
            Calculations.cat_database_set_up(bd['cat_facts'])
        return bd['cat_facts'].find_one({'id': int(random() * 20)})['text']

    @staticmethod
    def cat_database_set_up(cat_facts):
        req = requests.get('https://cat-fact.herokuapp.com/facts')
        if req.status_code != 200:
            return 'Error occurred'
        cat_facts.drop()
        json_facts = req.json()
        most_upvoted = sorted(json_facts['all'],
                              key=lambda fact: int(fact['upvotes']),
                              reverse=True)
        counter = 0
        for line in most_upvoted:
            line['id'] = counter
            counter += 1
        cat_facts.insert_many(most_upvoted)

    @staticmethod
    def get_horoscope(message: str):
        return get_horoscope_str(horo_message_parse(message))
