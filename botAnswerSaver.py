from telegram import Message
from typing import Dict, Optional
import json

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
        answers['s1'] = user_data['s1']

        answers['s2'] = user_data['s2']

        answers['part'] = user_data['part']

        index = 1
        while(True):
            key = str(index)
            answer = user_data.get(key, None)
            if answer is None:
                break

            answers[key] = answer
            index += 1

        answers['f1'] = user_data['f1']
        return answers

    user_info = get_user_info(user)
    answers = get_answers(user_data)
    user_answers_obj = {'user_info': user_info, 'answers': answers}
    filename = f'answers/{user.id}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json_str = json.dumps(user_answers_obj)
        f.write(json_str)
