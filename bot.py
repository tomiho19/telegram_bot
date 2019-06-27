# -*- coding: utf-8 -*-
#! /usr/bin/env python

import requests
import datetime
import sys
from time import sleep

DEFAULT_TOKEN = "805811490:AAG1E6fdfx-_mwLQbcqi4o29g0NCoVxhi-I"
URL = "https://api.telegram.org/bot%s/" % DEFAULT_TOKEN
USER_TEXT = ""

class Bot:
    def __init__(self, token=DEFAULT_TOKEN):
        self.token = token
        self.api_url = "https://api.telegram.org/bot%s/" % token

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        response = requests.get(self.api_url + method, params)
        result_json = response.json()['result']
        return result_json

    def get_last_update(self):
        get_result = self.get_updates()
        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]
        return last_update

    def get_chat_id(self, last_update):
         return last_update['message']['chat']['id']
    
    def send_message(self, chat_id, text):
        print('send_message')
        print(chat_id, text)
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        response = requests.post(self.api_url + method, params)
        print("Message {} has been sent to chat with id {}".format(text, chat_id))
        return response

greet_bot = Bot(DEFAULT_TOKEN)
greetings = ("hello", "world", "etc")
now = datetime.datetime.now()

def main():  
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        greet_bot.get_updates(new_offset)
        last_update = greet_bot.get_last_update()
        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']
        print(last_chat_text.lower() in greetings)
        print(today == now.day and 6 <= hour <= 12) 
        print(today == now.day and 17 <= hour <= 23)
        print(today == now.day and 12 <= hour <= 17)
        if last_chat_text.lower() in greetings and today == now.day and 6 <= hour <= 12:
            greet_bot.send_message(last_chat_id, 'Доброе утро животное %s, просыпайся пожалуйста смертный' % last_chat_name)
            today += 1
        elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour <= 17:
            greet_bot.send_message(last_chat_id, 'Добрый вечер бич сообщества, уже как бы вечер а ты все еще ничто лол, %s' % last_chat_name)
            today += 1
        elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour <= 23:
            greet_bot.send_message(last_chat_id, 'Ты все еще жив???? удивительно %s' % last_chat_name)
            today += 1

        new_offset = last_update_id + 1

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()
