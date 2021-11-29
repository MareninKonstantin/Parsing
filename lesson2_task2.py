# https://roscontrol.com/testlab/search?keyword=торт
import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint

product_find = input('Введите продукт: ')
pages = int(input('Введите количество страниц для обработки: '))

error = False
page = 1
products_list = []

while not error and page <= pages:
    url = 'https://roscontrol.com'
    params = {'keyword': product_find,
          'page': page}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

    response = requests.get(url + '/testlab/search', params=params, headers=headers)

    dom = BeautifulSoup(response.text, 'html.parser')

    try:
        nextbutton = dom.find('div', {'class': 'page-pagination'}).find('a', {'class': 'last'}).get('href')
    except:
        error = True

    products = dom.find_all('div', {'class', 'wrap-product-catalog__item'})

    for product in products:
        products_data = {}

        name = product.find('div', {'class': 'product__item-link'}).text
        try:
            rating = int(product.find('div', {'class': 'rating-value'}).text)
        except:
            rating = None

        features = product.find_all('div', {'class': 'row'})
        for feature in features:
            products_data[feature.find('div', {'class': 'text'}).text] = int(feature.find('div', {'class': 'right'}).text)

        products_data['name'] = name
        products_data['rating'] = rating
        products_data['site'] = url

        products_list.append(products_data)

    page += 1

pprint(products_list)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(products_list, f, ensure_ascii=False)
