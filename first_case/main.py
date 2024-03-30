import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json
import pprint as pp


data = pd.read_csv('data/data.csv', index_col=0)

# with open('data/cities.json', encoding='utf-8') as from_json:
#     cities = json.load(from_json)
#
# new_cities = []
# for city in cities:
#     new_cities.append({'city': city['city']})
#
#
# with open('data/cities_new.json', 'w', encoding='utf-8') as to_json:
#     json.dump(new_cities, to_json, ensure_ascii=False, indent=2)


with open('data/cities_new.json', encoding='utf-8') as from_json:
    cities = json.load(from_json)

cities_list = []
for city in cities:
    if type(city['city']) is list:
        cities_list.extend(city['city'])
    else:
        cities_list.append(city['city'])

# Идея заключается в том, что по идее нужно пропарсить сообщения на частоту использования тех или иных слов, а после
# удалять из сообщений и сравнивать со списком городов

result = []

for message in data['message']:
    message = message.lower()
    blacklist = ['цен', 'цвет', 'букет', 'достав', 'заказать', 'отправ', 'рождени',
                 'поздравлени', 'здравствуй', 'добрый день', 'привет', 'вариант',
                 'срочно', 'быстро', 'хочу', 'возможно', 'сдела', 'нужно', 'знаю',
                 'какие', 'подобрать', 'заказ', 'выбор', 'сегодня', 'день', 'сколько',
                 'стоит', 'только', 'послать', 'хотел', 'роз', 'акции', 'есть', 'вас',
                 'качество', 'надеюсь', 'юбилей', 'свадьб', 'орхиде', 'сможет', 'помоч',
                 'рекомендов', 'нибудь', 'красив', 'возможн', 'девушк', 'наличи', 'подскажите',
                 'для', 'свое', 'можно', 'завтра', 'хорош', 'будет', 'чтобы', 'потом', 'советовать',
                 'может', 'любит', 'вечер', 'утро', 'понедельник', 'гербер'
                 'выбор', 'спасибо', 'пожалуйста', ',', '.', '!', '?', '#']
    for element in blacklist:
        try:
            message = message.replace(element, '')
        except:
            pass
    temp = process.extract(message, cities_list, scorer=fuzz.token_set_ratio, limit=5)
    if temp[0][1] == 100:
        temp = [temp[0]]
    result.append(temp)
    # message_list = message.split(' ')
    # for element in message_list:
    #     if element not in ('', ' '):
    #         result = process.extractOne(element, cities_list, scorer=fuzz.token_set_ratio)
    #         if result[1] > 70:
    #             print(result)

data['possible_cities'] = result


data.to_csv('data/data_new.csv', encoding='utf-8')
