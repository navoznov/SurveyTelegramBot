#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import Message
from telegram.ext import CallbackContext
from typing import Dict, Optional
import json, os
from datetime import datetime
import helpers

def save_answer(message: Message, context: CallbackContext, question_id: str) -> None:
    if not message.voice is None:
        file_id = message.voice.file_id
        user_id = message.from_user.id
        # TODO: избавиться от захардкоженного ogg-формата, тут может быть и mp3 наверное
        filename = f'{user_id}/{file_id}.ogg'
        # TODO: вынести voices_dir_path в глобальную константу
        voices_dir_path ='answers/voices'
        file_path = os.path.join(voices_dir_path, filename)
        dir_path = os.path.dirname(file_path)
        helpers.check_dir_exists(dir_path)

        voice_file = context.bot.get_file(file_id)
        # TODO: загружать файлы в конце, а то вдруг юзер не закончит опрос
        voice_file.download(file_path)

        VOICE_METADATA_SEPARATOR = '***'
        metadata = ['voice', message.voice.mime_type, filename]
        context.user_data[question_id] = VOICE_METADATA_SEPARATOR.join(metadata)
    else:
        context.user_data[question_id] = message.text


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
        answers.update({k: v for k, v in user_data.items() if k.startswith('question')})
        answers['final1'] = user_data['final1']
        return answers

    user_info = get_user_info(user)
    answers = get_answers(user_data)
    answer_date = datetime.utcnow().replace(microsecond=0).isoformat()
    user_answers_obj = {'answer_date': answer_date, 'user_info': user_info, 'answers': answers}
    filename = f'answers/{user.id}.json'

    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(filename, 'w', encoding='utf-8') as f:
        json_str = json.dumps(user_answers_obj, ensure_ascii=False)
        f.write(json_str)


def get_all_answer_files():
    dir_path = 'answers'
    helpers.check_dir_exists(dir_path)
    file_paths = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    return file_paths


def get_all_answer_usernames():
    answer_file_paths = get_all_answer_files()
    usernames = [get_username_from_answer_file(f) for f in answer_file_paths]
    return [x for x in usernames if x != None]

def get_username_from_answer_file(file_path):
    json_str = open(file_path, 'r', encoding='utf-8').read()
    answer = json.loads(json_str)
    user_info = answer.get('user_info', None)
    if user_info == None:
        return None

    username = user_info.get('username', None)
    if username != None:
        return username

    return user_info.get('id', None)