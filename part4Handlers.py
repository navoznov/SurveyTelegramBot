#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import ParseMode, InputTextMessageContent, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Message
from telegram.ext import (
    Updater,
    CallbackContext,
    ConversationHandler
)
import messageTextProvider
import helpers
import states
import answerHelper

# РАЗДЕЛ 4
def part_4_question_1_handler(update: Update, context: CallbackContext) -> int:
    context.user_data['part_number'] = 4

    keys = [str(i+1) for i in range(12)] + ['4_1', '4_2', '8_yes_1', '8_no_1' ]
    keys.sort()
    keys = [f'question{key}' for key in keys]
    for key in keys:
        answerHelper.set_empty_answer(context.user_data, key)

    # TODO: а кнопка "свой вариант ответа" где? и как сделать? мб просто вариант "Другой"?
    text = 'Какой язык сейчас учите?'
    reply_keyboard = [['Английский', 'Немецкий', 'Нидерландский',
                       'Французский', 'Итальянский', 'Португальский', 'Испанский']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    helpers.get_message(update).reply_text(text, reply_markup=keyboard_markup)
    return states.PART_4_QUESTION_1_STATE


def part_4_question_2_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question1')
    text = '*Для чего* учите еще один новый язык?'
    message.reply_text(text, parse_mode='Markdown')
    return states.PART_4_QUESTION_2_STATE


def part_4_question_3_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question2')
    text = 'Как *ищете перевод* иностранного слова'
    message.reply_text(text, parse_mode='Markdown')
    return states.PART_4_QUESTION_3_STATE


def part_4_question_4_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question3')
    text = 'Бывают *сложности с поиском* правильного смысла перевода?'
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    message.reply_text(text, parse_mode='Markdown', reply_markup=keyboard_markup)
    context.user_data['state'] = states.PART_4_QUESTION_4_STATE
    return states.PART_4_QUESTION_4_STATE


def part_4_question_4_1_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question4')
    text = 'Как находили правильный перевод?'
    message.reply_text(text, parse_mode='Markdown')
    return states.PART_4_QUESTION_4_1_STATE


def part_4_question_4_2_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question4_1')
    text = 'Что помогает найти правильный смысл слова?'
    message.reply_text(text, parse_mode='Markdown')
    context.user_data['state'] = states.PART_4_QUESTION_4_2_STATE
    return states.PART_4_QUESTION_4_2_STATE


def part_4_question_5_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    if context.user_data['state'] == states.PART_4_QUESTION_4_STATE:
        answerHelper.save_answer(message, context, 'question4')
    elif context.user_data['state'] == states.PART_4_QUESTION_4_2_STATE:
        answerHelper.save_answer(message, context, 'question4_2')

    text = 'Какие *методики/приложения* используете чтобы запоминать новые слова?'
    message.reply_text(text, parse_mode='Markdown')
    return states.PART_4_QUESTION_5_STATE


def part_4_question_6_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question5')
    text = 'Какие еще *инструменты* используете для изучения языка в целом?'
    message.reply_text(text, parse_mode='Markdown')
    return states.PART_4_QUESTION_6_STATE


def part_4_question_7_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question6')
    text = 'Как *знание* других языков и *опыт* их изучения *помогает* с новым языком?'
    message.reply_text(text, parse_mode='Markdown')
    return states.PART_4_QUESTION_7_STATE


def part_4_question_8_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question7')
    text = 'Проверяете ли значение нового слова переводя на разные известные вам языки?'
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    message.reply_text(text, reply_markup=keyboard_markup)
    context.user_data['state'] = states.PART_4_QUESTION_8_STATE
    return states.PART_4_QUESTION_8_STATE


def part_4_question_8_yes_1_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question8')
    text = 'Чем полезно проверять перевод нового слова сразу на несколько языков?'
    message.reply_text(text, parse_mode='Markdown')
    context.user_data['state'] = states.PART_4_QUESTION_8_YES_1_STATE
    return states.PART_4_QUESTION_8_YES_1_STATE


def part_4_question_8_no_1_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question8')
    text = 'Как узнаете смысл слова? Переводите обычно только на свой родной язык или как-то иначе?'
    message.reply_text(text, parse_mode='Markdown')
    context.user_data['state'] = states.PART_4_QUESTION_8_NO_1_STATE
    return states.PART_4_QUESTION_8_NO_1_STATE


def part_4_question_9_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    if context.user_data['state'] == states.PART_4_QUESTION_8_YES_1_STATE:
        answerHelper.save_answer(message, context, 'question8_yes_1')
    elif context.user_data['state'] == states.PART_4_QUESTION_8_NO_1_STATE:
        answerHelper.save_answer(message, context, 'question8_no_1')

    text = 'Что бы хотели улучшить, *сделать более эффективным*, в процессе изучения языка?'
    message.reply_text(text, parse_mode='Markdown')
    return states.PART_4_QUESTION_9_STATE


def part_4_question_10_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question9')
    text = 'Как отслеживаете свой *текущий уровень* в изучении нового языка?'
    message.reply_text(text, parse_mode='Markdown')
    return states.PART_4_QUESTION_10_STATE


def part_4_question_11_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question10')
    text = 'Отслеживаете текущее количество известных слов? Если да, то как?'
    message.reply_text(text, parse_mode='Markdown')
    return states.PART_4_QUESTION_11_STATE


def part_4_question_12_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question11')
    text = 'Что вас *мотивирует* изучать новый язык?'
    message.reply_text(text, parse_mode='Markdown')
    return states.PART_4_QUESTION_12_STATE


def part_4_survey_finish_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question12')
    text = messageTextProvider.get_survey_finish_state_text()
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    message.reply_text(text, reply_markup=keyboard_markup)
    context.user_data['state'] = states.SURVEY_FINISH_STATE
    return states.SURVEY_FINISH_STATE