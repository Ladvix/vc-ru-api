import api
import json
from utils import dirs, session, anon_account
from utils.publisher import Publisher


if __name__ == '__main__':
    client = api.Client()
    
    try:
        # Загрузка куки и refresh токена в текущую сессию из файла
        client.session.cookies.update(session.load_cookies())
        client.session.refresh_token = session.load_refresh_token()

        refresh_response = json.loads(client.refresh().text)
        client.session.jwtoken = refresh_response['data']['accessToken']

        # Публикация поста
        publisher = Publisher(client)
        publisher.add_block(
            block_type='text', 
            hidden=False, 
            anchor='', 
            content={
                'text': 'Не менее интересный текст.'
            }
        )

        post_response = publisher.post('Некоторый интереснейший заголовок.')

    except:
        # Регистрация анонимного аккаунта
        name = input('Имя >> ')
        anon_account.register(client, name)