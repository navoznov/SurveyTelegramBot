#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import Message
from typing import Dict, Optional
import json
import os

def save_answer(message: Message, user_data: Optional[Dict], question_id: str) -> None:
    if not message.voice is None:
        VOICE_METADATA_SEPARATOR = '***'
        print(message.voice.mime_type)
        user_data[question_id] = [message.voice.mime_type, message.voice.file_id].join(VOICE_METADATA_SEPARATOR)
    else:
        user_data[question_id] = message.text


def set_empty_answer(user_data: Optional[Dict], question_id: str) -> None:
    user_data[question_id] = ''


def save_user_answers_to_file(user: Optional['User'], user_data: Optional[Dict]) -> None:
    def get_user_info(user):
        return {
            'id': user.id,
            'language_code': user.language_code,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'link': user.link,
        }

    def get_answers(user_data):
        answers = {}
        answers['start1'] = user_data['start1']
        answers['start2'] = user_data['start2']
        answers['part_number'] = user_data['part_number']

        index = 1
        while(True):
            key = f'question{index}'
            answer = user_data.get(key, None)
            if answer is None:
                break

            answers[key] = answer
            index += 1

        answers['final1'] = user_data['final1']
        return answers

    user_info = get_user_info(user)
    answers = get_answers(user_data)
    user_answers_obj = {'user_info': user_info, 'answers': answers}
    filename = f'answers/{user.id}.json'
    if not os.path.exists(answers_directory_name):
        os.makedirs(os.path.dirname(filename))

    with open(filename, 'w', encoding='utf-8') as f:
        json_str = json.dumps(user_answers_obj, ensure_ascii=False)
        f.write(json_str)