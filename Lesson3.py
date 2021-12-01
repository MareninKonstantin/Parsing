# https://kirov.hh.ru/search/vacancy?area=49&fromSearchLine=true&text=python
import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['hh']
vacancies_mongo = db.vacancies

#---Функция добавления новой вакансии---
def new_vacancy(doc):
    lnk = doc['link']
    if vacancies_mongo.count_documents({'link': lnk}) > 0:
        print('Error! The vacancy is duplicated!')
    else:
        vacancies_mongo.insert_one(doc)

#---Функция поиска вакансии с заработной платой больше введённой суммы---
def findvacancy(salary):
    vacancies_mongo_find = list(vacancies_mongo.find({'$or': [{'max_salary': {'$gt': salary}}, {'min_salary': {'$gt': salary}}]}))
    for doc in vacancies_mongo_find:
        pprint(doc)

position = input('Введите должность: ')
pages = int(input('Введите количество страниц для обработки: '))

error = False
page = 0
vacancies_list = []

while not error and page < pages:
    url = 'https://kirov.hh.ru'
    params = {'area': '49',
          'fromSearchLine': 'true',
          'text': position,
          'page': page}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

    response = requests.get(url + '/search/vacancy', params=params, headers=headers)

    dom = BeautifulSoup(response.text, 'html.parser')

    try:
        nextbutton = dom.find('div', {'class': 'pager'}).find('a', {'class': 'bloko-button'}).get('href')
    except:
        error = True

    vacancies = dom.find_all('div', {'class', 'vacancy-serp-item'})

    for vacancy in vacancies:
        vacancy_data = {}

        name = vacancy.find('a').text
        link = vacancy.find('a', {'class': 'bloko-link'}).get('href')

        try:
            salary_info = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).text
            salary_info = salary_info.split()
            info = False
            for i in salary_info:
                if i.isdigit():
                    info = True
            if not info:
                min_salary = None
                max_salary = None
                currency = None
            elif salary_info[0] == 'от':
                min_salary = int(salary_info[1] + salary_info[2])
                max_salary = None
                currency = salary_info[3]
            elif salary_info[0] == 'до':
                min_salary = None
                max_salary = int(salary_info[1] + salary_info[2])
                currency = salary_info[3]
            else:
                min_salary = int(salary_info[0] + salary_info[1])
                max_salary = int(salary_info[3] + salary_info[4])
                currency = salary_info[5]
        except:
            min_salary = None
            max_salary = None
            currency = None


        vacancy_data['name'] = name
        vacancy_data['min_salary'] = min_salary
        vacancy_data['max_salary'] = max_salary
        vacancy_data['currency'] = currency
        vacancy_data['link'] = link
        vacancy_data['site'] = url

        vacancies_list.append(vacancy_data)
        new_vacancy(vacancy_data)
    page += 1

for doc in vacancies_mongo.find({}):
    pprint(doc)

salary = int(input('Введите минимальный уровень зарплаты: '))
findvacancy(salary)

with open('data.json', 'w', encoding='utf-8') as f:
   json.dump(vacancies_list, f, ensure_ascii=False)