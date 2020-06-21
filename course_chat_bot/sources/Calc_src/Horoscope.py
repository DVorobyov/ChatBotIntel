import requests as req
import re

Zod_sign_dict = {
    'овен': 'aries',
    'телец': 'taurus',
    'близнецы': 'gemini',
    'рак': 'cancer',
    'лев': 'leo',
    'дева': 'virgo',
    'весы': 'libra',
    'скорпион': 'scorpio',
    'стрелец': 'sagittarius',
    'козерог': 'capricorn',
    'водолей': 'aquarius',
    'рыбы': 'pisces',
}


def horo_message_parse(message: str):
    if len(re.split(r'\s', message)) > 1:
        return re.split(r'\s', message)[1]
    else:
        return None


def get_horoscope_str(zod_sign: str):
    try:
        zod_sign = Zod_sign_dict[zod_sign.lower()]
    except BaseException:
        return 'Check input'
    try:
        data = req.get(f'https://horo.mail.ru/prediction/{zod_sign}/today/')
        return _horo_html_parse(data)
    except BaseException:
        return 'Internet source error occurred'


def _horo_html_parse(data: req.Response):
    str_data = re.search(r'<div class="article__item article__item_alignment_left article__item_html"><p>(.|\s)*?\<\/d',
                       data.text).group(0)
    return re.split(r'(\<|\>)', str_data)[8] + re.split(r'(\<|\>)', str_data)[16]

