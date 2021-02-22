from telegram import Message
from typing import Dict, Optional

def save_answer(message: Message, user_data:Optional[Dict], part: int, question_id: str):
    if not message.voice is None:
        VOICE_METADATA_SEPARATOR = '***'
        print(message.voice.mime_type)
        user_data[question_id] = [message.voice.mime_type, message.voice.file_id].join(VOICE_METADATA_SEPARATOR)
    else:
        user_data[question_id] = message.text
    pass
