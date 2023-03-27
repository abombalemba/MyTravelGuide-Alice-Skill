from flask import Flask, request, render_template
from json import dumps
from random import choice
from database import *


app = Flask(__name__)
session_storage = {}


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/post', methods=['POST'])
def post():
    return dumps(handler(request.json))


def handler(req):
    global session_storage
    user_id = req['session']['user_id']

    response = {
        'version': req['version'],
        'session': req['session'],
        'response': {
            'end_session': 'false'
        }
    }

    if req['session']['new']:
        print(1, req['request']['original_utterance'])

        session_storage[user_id] = {
            'location': '2',
            'country': ''
        }

        text = choice(alice_phrase1)

        response['response']['text'] = text
        response['response']['tts'] = text
        response['response']['buttons'] = get_suggests('yes/no')
        response['response']['location'] = '2'

    elif user_id in session_storage.keys() and session_storage[user_id]['location'] == '2':
        print(2, req['request']['original_utterance'])

        if req['request']['original_utterance'].lower() in user_access:
            session_storage[user_id]['location'] = '3'
            text = choice(alice_phrase2)

            response['response']['text'] = text
            response['response']['tts'] = text
            response['response']['buttons'] = get_suggests('countries')

        elif req['request']['original_utterance'].lower() in user_refused:
            session_storage[user_id]['location'] = '2.1'
            text = choice(alice_phrase_dop1)

            response['response']['text'] = text
            response['response']['tts'] = text
            response['response']['buttons'] = get_suggests('ready')

    elif user_id in session_storage.keys() and session_storage[user_id]['location'] == '2.1':
        print(2.1, req['request']['original_utterance'])

        if req['request']['original_utterance'].lower() in user_ready:
            session_storage[user_id]['location'] = '3'
            text = choice(alice_phrase2)

            response['response']['text'] = text
            response['response']['tts'] = text
            response['response']['buttons'] = get_suggests('countries')

    elif user_id in session_storage.keys() and session_storage[user_id]['location'] == '3':
        print(3, req['request']['original_utterance'].lower().title())

        if req['request']['original_utterance'].lower().title() in countries.keys():
            session_storage[user_id]['location'] = '4'
            country = req['request']['original_utterance'].lower().title()
            session_storage[user_id]['country'] = country
            text = choice(alice_phrase3).format(countries[session_storage[user_id]['country']][0][1])

            response['response']['text'] = text
            response['response']['tts'] = text
            response['response']['buttons'] = get_suggests('yes/no')
            response['response']['card'] = get_card(session_storage[user_id]['country'], text, 0)

        else:
            text = choice(alice_phrase_dop2)

            response['response']['text'] = text
            response['response']['tts'] = text
            response['response']['buttons'] = get_suggests('countries')

    elif user_id in session_storage.keys() and session_storage[user_id]['location'] == '4':
        print(4, req['request']['original_utterance'])

        if req['request']['original_utterance'].lower() in user_access:
            session_storage[user_id]['location'] = '5'
            text = choice(alice_phrase4).format(countries[session_storage[user_id]['country']][1][1])

            response['response']['text'] = text
            response['response']['tts'] = text
            response['response']['buttons'] = get_suggests('yes/no')
            response['response']['card'] = get_card(session_storage[user_id]['country'], text, 1)

        else:
            text = choice(alice_phrase_dop3)
            del session_storage[user_id]

            response['response']['text'] = text
            response['response']['tts'] = text
            response['response']['end_session'] = 'true'

    elif user_id in session_storage.keys() and session_storage[user_id]['location'] == '5':
        print(5, req['request']['original_utterance'])

        if req['request']['original_utterance'].lower() in user_access:
            session_storage[user_id]['location'] = '6'
            text = choice(alice_phrase5).format(countries[session_storage[user_id]['country']][2][1])

            response['response']['text'] = text
            response['response']['tts'] = text
            response['response']['buttons'] = get_suggests('yes/no')
            response['response']['card'] = get_card(session_storage[user_id]['country'], text, 2)

        else:
            text = choice(alice_phrase_dop3)
            del session_storage[user_id]

            response['response']['text'] = text
            response['response']['tts'] = text
            response['response']['end_session'] = 'true'

    elif user_id in session_storage.keys() and session_storage[user_id]['location'] == '6':
        print(6, req['request']['original_utterance'])

        if req['request']['original_utterance'].lower() in user_access:
            session_storage[user_id]['location'] = '3'
            text = choice(alice_phrase2)

            response['response']['text'] = text
            response['response']['tts'] = text
            response['response']['buttons'] = get_suggests('countries')

        else:
            text = choice(alice_phrase_dop3)
            del session_storage[user_id]

            response['response']['text'] = text
            response['response']['tts'] = text
            response['response']['end_session'] = 'true'

    else:
        response['response']['text'] = text_error
        response['response']['tts'] = text_error
        response['response']['end_session'] = 'true'

    return response


def get_suggests(what):
    if what == 'yes/no':
        suggests = list({'title': button, 'hide': True} for button in user_yes_no)
    elif what == 'countries':
        suggests = list({'title': button, 'hide': True} for button in countries.keys())
    elif what == 'ready':
        suggests = list({'title': button, 'hide': True} for button in user_ready)
    else:
        suggests = []

    return suggests


def get_card(country, text, num):
    return {
        'type': 'BigImage',
        'image_id': countries[country][num][2],
        'title': countries[country][num][0],
        'description': text
    }


if __name__ == '__main__':
    app.run()
