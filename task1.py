import json
import requests
from pprint import pprint

#формирование запроса
url = 'https://api.github.com/users/'
owner = 'MareninKonstantin'

response = requests.get(f'{url}{owner}/repos')

#вывод результата на экран
for key in response.json():
    print(key['name'])

#выгрузка результата в файл
with open('data.json', 'w') as f:
    json.dump(response.json(), f)