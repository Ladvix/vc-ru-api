import json
import requests


BASE_URL = 'https://api.vc.ru'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'

class Client():

    def __init__(self):
        '''Инициализация клиента'''
        self.session = requests.Session()


    def register(self, name, email, password):
        '''API метод register
        
        Регистрация аккаунта
        '''
        fields = {
            ('name', (None, name)),
            ('email', (None, email)),
            ('password', (None, password))
        }
        headers = {
            'User-Agent': USER_AGENT
        }

        response = self.session.post(BASE_URL + '/v3.4/auth/email/register', files=fields, headers=headers)

        return response
    
    
    def sessions(self):
        '''API метод sessions'''
        fields = {
            ('referer', (None, 'email'))
        }
        headers = {
            'User-Agent': USER_AGENT
        }

        response = self.session.post(BASE_URL + '/v2.6/sessions', files=fields, headers=headers)

        return response
    

    def confirm(self, token):
        '''API метод confirm
        
        Подтверждение почты
        '''
        fields = {
            ('token', (None, token))
        }
        headers = {
            'User-Agent': USER_AGENT
        }

        response = self.session.post(BASE_URL + '/v3.4/auth/email/confirm', files=fields, headers=headers)

        return response
    

    def login(self, email, password):
        '''API метод login
        
        Вход в аккаунт
        '''
        fields = {
            ('email', (None, email)),
            ('password', (None, password))
        }
        headers = {
            'User-Agent': USER_AGENT
        }

        response = self.session.post(BASE_URL + '/v3.4/auth/email/login', files=fields, headers=headers)
        
        return response
    

    def me(self):
        '''API метод me
        
        Получение основных данных аккаунта
        '''
        headers = {
            'User-Agent': USER_AGENT,
            'Jwtauthorization': 'Bearer ' + self.session.jwtoken
        }

        response = self.session.get(BASE_URL + '/v2.1/subsite/me', headers=headers)

        return response
    

    def refresh(self):
        '''API метод refresh
        
        Обновление jwtoken и refreshToken
        '''
        fields = {
            ('token', (None, self.session.refresh_token))
        }
        headers = {
            'User-Agent': USER_AGENT
        }

        response = self.session.post(BASE_URL + '/v3.4/auth/refresh', files=fields, headers=headers)

        return response
    

    def editor(self, entry):
        '''API метод editor
        
        Редактирование черновика
        '''
        fields = {
            ('entry', (None, json.dumps(entry, ensure_ascii=False)))
        }
        headers = {
            'User-Agent': USER_AGENT,
            'Jwtauthorization': 'Bearer ' + self.session.jwtoken
        }

        response = self.session.post(BASE_URL + '/v2.1/editor', files=fields, headers=headers)

        return response
    

    def publish(self, id):
        '''API метод publish

        Публикация на страницу
        '''
        headers = {
            'User-Agent': USER_AGENT,
            'Jwtauthorization': 'Bearer ' + self.session.jwtoken
        }

        response = self.session.post(BASE_URL + f'/v2.1/editor/{id}/publish', headers=headers)

        return response
    

    def upload(self, id):
        '''API метод upload
        
        Загрузка фото/видео на сервер vc.ru
        '''
        headers = {
            'User-Agent': USER_AGENT,
            'Jwtauthorization': 'Bearer ' + self.session.jwtoken
        }

        response = self.session.post(BASE_URL + f'/v2.1/editor/{id}/publish', headers=headers)

        return response