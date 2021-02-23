#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from telegram import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Message
from telegram.ext import (
    Updater,
    CallbackContext,
    ConversationHandler
)
import shutil, os

from options import Options
import botMessageProvider, botStates, helpers, botAnswerSaver
import botPart1Handlers, botPart2Handlers, botPart3Handlers, botPart4Handlers
import export

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start_state_handler(update: Update, context: CallbackContext) -> int:
    # TODO: проверить, проходил ли юзер раньше этот опрос. если проходил то надо предупредить что ответы перезапишутся

    text = botMessageProvider.get_start_state_text()
    reply_keyboard = [['Начнем']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    helpers.get_message(update).reply_text(text, reply_markup=keyboard_markup)
    return botStates.START_STATE


def survey_finish_handler(update: Update, context: CallbackContext) -> int:
    text = botMessageProvider.get_survey_finish_state_text()
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    helpers.get_message(update).reply_text(text, reply_markup=keyboard_markup)
    context.user_data['state'] = botStates.SURVEY_FINISH_STATE
    return botStates.SURVEY_FINISH_STATE


def plans_info_handler(update: Update, context: CallbackContext) -> int:
    text = botMessageProvider.get_plans_info_state_text()
    helpers.get_message(update).reply_text(text, parse_mode='Markdown')
    context.user_data['state'] = botStates.PLANS_INFO_STATE
    return botStates.PLANS_INFO_STATE


def total_finish_handler(update: Update, context: CallbackContext) -> int:
    if context.user_data['state'] == botStates.PLANS_INFO_STATE:
        botAnswerSaver.save_answer(update.message, context, 'final1')
    else:
        botAnswerSaver.set_empty_answer(context.user_data, 'final1')

    botAnswerSaver.save_user_answers_to_file(update.effective_user, context.user_data)

    text = 'Теперь точно всё :) Спасибо и до скорых встреч!'
    helpers.get_message(update).reply_text(text, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def question_1_handler(update: Update, context: CallbackContext) -> int:
    text = botMessageProvider.get_question_1_state_text()
    reply_keyboard = [['1', '2'], ['3', 'Больше трех']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    helpers.get_message(update).reply_text(text, reply_markup=keyboard_markup)
    return botStates.QUESTION_1_STATE


def question_2_handler(update: Update, context: CallbackContext) -> int:
    def parse_answer(answer):
        language_count, success = helpers.intTryParse(answer)
        if not success:
            answer_mapping = {'1': 1, '2': 2, '3': 3, 'Больше трех': 4}
            language_count = answer_mapping.get(answer, -1)
        return language_count

    message = helpers.get_message(update)
    language_count = parse_answer(message.text)
    if language_count == -1:
        return botStates.QUESTION_1_STATE

    context.user_data['language_count'] = language_count
    context.user_data['start1'] = language_count

    text = botMessageProvider.get_question_2_state_text()
    reply_keyboard = [['Нет, не изучаю', 'Да, изучаю']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    message.reply_text(text, reply_markup=keyboard_markup)
    return botStates.QUESTION_2_STATE


def fork_handler(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    language_count = user_data['language_count']

    NO = 'нет'
    YES = 'да'
    answer = update.message.text.lower()
    if NO in answer:
        user_data['start2'] = NO

        if language_count == 1:
            # Раздел 1
            return botPart1Handlers.part_1_question_1_handler(update, context)
        else:
            # Раздел 3
            return part_3_question_1_handler(update, context)
    elif YES in answer:
        user_data['start2'] = YES

        if language_count == 1:
            # Раздел 2
            return botPart2Handlers.part_2_question_1_handler(update, context)
        else:
            # Раздел 4
            return botPart4Handlers.part_4_question_1_handler(update, context)
    else:
        return botStates.QUESTION_2_STATE


def admin_state_handler(update: Update, context: CallbackContext, admin_ids) -> int:
    user = helpers.get_message(update).from_user
    logger.info(f'@{user.username} tried to log in to the admin area')
    if user.id not in admin_ids:
        return botStates.START_STATE

    text = 'Вы вошли в админку.'
    reply_keyboard = [['Получить список проголосовавших'], ['Экспорт результатов в HTML']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    helpers.get_message(update).reply_text(text, reply_markup=keyboard_markup)
    return botStates.ADMIN_STATE


def admin_get_answers_list_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    user = message.from_user
    logger.info(f'@{user.username} listed usernames')

    usernames = botAnswerSaver.get_all_answer_usernames()
    text = '\n'.join([f'@{x}' for x in usernames])
    reply_keyboard = [['Вернуться в главное меню админки']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    message.reply_text(text, parse_mode='Markdown', reply_markup=keyboard_markup, reply_to_message_id=message.message_id)
    return botStates.ADMIN_USERNAME_LIST_STATE


def admin_export_state_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    user = message.from_user
    logger.info(f'@{user.username} exported survey results')

    export_dir_path = export.Export().export_to_html(user.id)
    export_dir_path = os.path.normpath(export_dir_path)
    archive_file_name = os.path.split(export_dir_path)[-1]
    zip_file = shutil.make_archive(archive_file_name, 'zip', root_dir=export_dir_path, base_dir='.',)

    reply_keyboard = [['Вернуться в главное меню админки']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    with open(zip_file, 'rb') as f:
        message.reply_document(f, reply_markup=keyboard_markup, reply_to_message_id=message.message_id)

    os.remove(zip_file)
    return botStates.ADMIN_EXPORT_RESULT_STATE


def cancel(update: Update, context: CallbackContext) -> int:
    pass

