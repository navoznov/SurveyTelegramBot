#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import ParseMode, InputTextMessageContent, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Message
from telegram.ext import (
    Updater,
    CallbackContext,
    ConversationHandler
)
import botMessageProvider
import helpers
import botStates
import botAnswerSaver

# РАЗДЕЛ 3
def part_3_question_1_handler(update: Update, context: CallbackContext) -> int:
    context.user_data['part_number'] = 3

    keys = [str(i+1) for i in range(7)] + ['4_1', '4_2', '4_3', '5_1', '5_2', '5_3']
    keys.sort()
    keys = [f'question{key}' for key in keys]
    for key in keys:
        botAnswerSaver.set_empty_answer(context.user_data, key)

    text = 'Какие инструменты использовали для запоминания новых слов?'
    helpers.get_message(update).reply_text(text)
    return botStates.PART_3_QUESTION_1_STATE


def part_3_question_2_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    botAnswerSaver.save_answer(message, context, 'question1')
    text = 'Как искали перевод иностранного слова?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_3_QUESTION_2_STATE


def part_3_question_3_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    botAnswerSaver.save_answer(message, context, 'question2')
    text = 'Бывали проблемы с поиском правильного смысла перевода? Как находили верный перевод?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_3_QUESTION_3_STATE


def part_3_question_4_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    botAnswerSaver.save_answer(message, context, 'question3')
    text = 'Когда-нибудь проверяли сколько вы знаете слов?'
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    message.reply_text(text, reply_markup=keyboard_markup)
    context.user_data['state'] = botStates.PART_3_QUESTION_4_STATE
    return botStates.PART_3_QUESTION_4_STATE


def part_3_question_4_1_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    botAnswerSaver.save_answer(message, context, 'question4')
    text = 'Сколько примерно слов сейчас знаете?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_3_QUESTION_4_1_STATE


def part_3_question_4_2_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    botAnswerSaver.save_answer(message, context, 'question4_1')
    text = 'Чем пользовались чтобы узнать это число?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_3_QUESTION_4_2_STATE


def part_3_question_4_3_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    botAnswerSaver.save_answer(message, context, 'question4_2')
    text = 'Продолжаете набирать словарный запас?'
    message.reply_text(text, parse_mode='Markdown')
    context.user_data['state'] = botStates.PART_3_QUESTION_4_3_STATE
    return botStates.PART_3_QUESTION_4_3_STATE


def part_3_question_5_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    if context.user_data['state'] == botStates.PART_3_QUESTION_4_3_STATE:
        botAnswerSaver.save_answer(message, context, 'question4_3')
    elif context.user_data['state'] == botStates.PART_3_QUESTION_4_STATE:
        botAnswerSaver.save_answer(message, context, 'question4')

    text = 'Планируете изучать новый язык?'
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    message.reply_text(text, reply_markup=keyboard_markup)
    context.user_data['state'] = botStates.PART_3_QUESTION_5_STATE
    return botStates.PART_3_QUESTION_5_STATE


def part_3_question_5_1_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    botAnswerSaver.save_answer(message, context, 'question5')
    text = 'Что вас останавливает?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_3_QUESTION_5_1_STATE


def part_3_question_5_2_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    botAnswerSaver.save_answer(message, context, 'question5_1')
    text = 'Как думаете, вам поможет знание двух языков в изучении третьего? Если да, то чем?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_3_QUESTION_5_2_STATE


def part_3_question_5_3_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    botAnswerSaver.save_answer(message, context, 'question5_2')
    text = 'С чего начнёте учить новый язык?'
    message.reply_text(text, parse_mode='Markdown')
    context.user_data['state'] = botStates.PART_3_QUESTION_5_3_STATE
    return botStates.PART_3_QUESTION_5_3_STATE


def part_3_question_6_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    if context.user_data['state'] == botStates.PART_3_QUESTION_5_3_STATE:
        botAnswerSaver.save_answer(message, context, 'question5_3')
    elif context.user_data['state'] == botStates.PART_3_QUESTION_5_STATE:
        botAnswerSaver.save_answer(message, context, 'question5')

    text = 'Какой мотивации не хватает чтобы начать изучать новый язык?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_3_QUESTION_6_STATE


def part_3_survey_finish_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    botAnswerSaver.save_answer(message, context, 'question6')
    text = botMessageProvider.get_survey_finish_state_text()
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    message.reply_text(text, reply_markup=keyboard_markup)
    context.user_data['state'] = botStates.SURVEY_FINISH_STATE
    return botStates.SURVEY_FINISH_STATE
