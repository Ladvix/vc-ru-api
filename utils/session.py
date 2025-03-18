import json
import pickle
from utils import dirs, json_helper


COOKIES_FILE = 'cookies.pkl'
REFRESH_TOKEN_FILE = 'refresh_token.txt'
CREDENTIALS_FILE = 'credentials.json'

def save_cookies(cookies):
    '''Сохранение куки текущей сессии в файл'''
    with open(dirs.ABS_PATH + 'session/' + COOKIES_FILE, 'wb') as f:
        pickle.dump(cookies, f)

def load_cookies():
    '''Загрузка куки в текущую сессию из файла'''
    with open(dirs.ABS_PATH + 'session/' + COOKIES_FILE, 'rb') as f:
        return pickle.load(f)

def save_refresh_token(refresh_token):
    '''Сохранение refresh_token текущей сессии в файл'''
    with open(dirs.ABS_PATH + 'session/' +  REFRESH_TOKEN_FILE, 'w') as f:
        f.write(refresh_token)

def load_refresh_token():
    '''Загрузка refresh_token текущей сессии из файла'''
    with open(dirs.ABS_PATH + 'session/' +  REFRESH_TOKEN_FILE, 'r') as f:
        return f.read()

def save_credentials(name, email, password):
    '''Сохранение аутентификационных данных'''
    credentials = {
        'name': name,
        'email': email,
        'password': password
    }

    json_helper.write(dirs.ABS_PATH + 'session/' +  CREDENTIALS_FILE, credentials)