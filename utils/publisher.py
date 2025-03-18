import json
from utils import dirs, json_helper


class Publisher():

    def __init__(self, client):
        self.client = client
        self.blocks = []


    def add_block(self, block_type, hidden, anchor, content):
        '''Добавить блок контента

        >>> block_type = "" # Тип блока
        >>> hidden = "" # true/false - Скрыть блок
        >>> anchor = "" # left/right - Выравнивание

        Типы блоков:
        
        1. text - Текст
        >>> content = {
            text = ""
        }
        
        2. header - Заголовок
        >>> content = {
            text = "",
            style = "" # h1/h2/h3
        },
        '''
        if block_type == 'text':
            text = content['text']

            self.blocks.append({
                'type': 'text',
                'data': {
                    'text': f'<p>{text}</p>'
                },
                'cover': False,
                'hidden': hidden,
                'anchor': anchor
            })
        elif block_type == 'header':
            style = content['style']
            text = content['text']

            self.blocks.append({
                'type': 'text',
                'data': {
                    'style': content['style'],
                    'text': content['text']
                },
                'cover': False,
                'hidden': hidden,
                'anchor': anchor
            })


    def post(self, title):
        '''Публикация поста, верстка статьи'''
        me_response = json.loads(self.client.me().text)

        entry = json_helper.read(dirs.ABS_PATH + 'samples/entry.json')

        entry['title'] = title
        entry['user_id'] = me_response['result']['id']
        entry['subsite_id'] = me_response['result']['id']
        entry['entry']['blocks'] = self.blocks

        editor_response = json.loads(self.client.editor(entry).text)
        post_id = editor_response['result']['entry']['id']

        publish_response = self.client.publish(post_id)

        return publish_response