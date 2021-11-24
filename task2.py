#https://vk.com/id5505187
#Приложение 8009461
#access_token=f90d8f154ad7039fd55e70ccd856d146a2ba82044b487dace1907e94aa3c7fa0672e44dd4b58c4506bd60&
# expires_in=86400&
# user_id=5505187

import json
import requests

#создание запроса
url = "https://api.vk.com/method/friends.get"
usr = 5505187
token = 'f90d8f154ad7039fd55e70ccd856d146a2ba82044b487dace1907e94aa3c7fa0672e44dd4b58c4506bd60'
params = {'user_ids': usr, 'access_token': token, 'v': '5.131', 'fields': 'nickname'}

#результат запроса
response = requests.get(url, params=params)

#фильтрация информации о друзьях
rsp = response.json()['response']['items']

#Вывод фамилии и имени
for key in rsp:
    print(f'{key["last_name"]} {key["first_name"]}')

rsp = json.dumps(rsp)

#выгрузка в файл
with open('data2.json', 'w') as f:
    json.dump(rsp, f)