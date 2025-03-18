import json
import string
import time
import random
import requests
import quopri
from urllib.parse import parse_qs, urlparse
from bs4 import BeautifulSoup
from utils import session


BASE_URL = 'https://api.mail.tm' # или 'https://api.mail.gw'

def register(client, name):
    '''Регистрация анонимного аккаунта по почте'''

    # Получаем список доступных доменов
    response = requests.get(BASE_URL + '/domains')

    if response.status_code == 200:
        # Выбираем случайный домен
        domains_list = json.loads(response.text)['hydra:member']
        domain = domains_list[random.randint(0, len(domains_list) - 1)]['domain']

        # Генерируем почтовый адрес и пароль
        email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '@' + domain
        password = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))

        # Регистрация почты
        accounts = requests.post(BASE_URL + '/accounts', json={'address': email, 'password': password})
        token = json.loads(requests.post(BASE_URL + '/token', json={'address': email, 'password': password}).text)['token']

        response = client.register(name, email, password)

        if response.status_code == 200:
            # Заглушка, ожидание письма
            time.sleep(5)

            # Обработка сообщения
            messages = requests.get(BASE_URL + '/messages', headers={'Authorization': 'Bearer ' + token})
            url = json.loads(messages.text)['hydra:member'][0]['downloadUrl']
            
            message_content = requests.get(BASE_URL + url, headers={'Authorization': 'Bearer ' + token})
            message_content = quopri.decodestring(message_content.text)
            soup = BeautifulSoup(message_content, features = 'html.parser')
            html_content = soup.find_all('a', {'class': 'button button--1'})

            for e in html_content:
                # Получаем токен для подтверждения e-mail
                token = parse_qs(urlparse(e.get('href')).query).get('token')
                client.session.get(e.get('href'))

                # Подтверждаем e-mail
                sessions = client.sessions()
                confirm = client.confirm(token[0])

                # Получаем Jwtoken для авторизации
                client.session.jwtoken = json.loads(confirm.text)['data']['accessToken']

                # Получаем RefreshToken для авторизации
                client.session.refresh_token = json.loads(confirm.text)['data']['refreshToken']
                
                # Сохраняем необходимые данные
                session.save_cookies(client.session.cookies)
                session.save_refresh_token(client.session.refresh_token)
                session.save_credentials(name, email, password)
                
                return {
                    'name': name,
                    'email': email,
                    'password': password
                }
        else:
            response = json.loads(response.text)
            message = response['message']
            code = response['code']
            
            print(f'[{code}] Произошла ошибка на стороне API: {message}')
    else:
        response = json.loads(response.text)
        message = response['message']
        code = response['code']

        print(f'[{code}] Произошла ошибка на стороне API: {message}')