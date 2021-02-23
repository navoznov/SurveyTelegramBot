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
import answerHelper

# РАЗДЕЛ 2
def part_2_question_1_handler(update: Update, context: CallbackContext) -> int:
    context.user_data['part_number'] = 2

    keys = [f'question{i+1}' for i in range(7)]
    for key in keys:
        answerHelper.set_empty_answer(context.user_data, key)

    text = '*Для чего* учите новый язык?'
    helpers.get_message(update).reply_text(text, parse_mode='Markdown')
    return botStates.PART_2_QUESTION_1_STATE


def part_2_question_2_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question1')
    text = 'Как *ищете перевод* иностранного слова?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_2_QUESTION_2_STATE


def part_2_question_3_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question2')
    text = 'Какие *инструменты* используете для запоминания новых слов?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_2_QUESTION_3_STATE


def part_2_question_4_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question3')
    text = 'Бывают *проблемы с поиском* правильного смысла перевода?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_2_QUESTION_4_STATE


def part_2_question_5_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question4')
    text = 'Насколько вам важна *эффективность* процесса изучения языка?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_2_QUESTION_5_STATE


def part_2_question_6_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question5')
    text = 'Как отслеживаете свой *текущий прогресс* в изучении нового языка?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_2_QUESTION_6_STATE


def part_2_question_7_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question6')
    text = 'Что вас *мотивирует* изучать новый язык?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_2_QUESTION_7_STATE


def part_2_survey_finish_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question7')
    text = botMessageProvider.get_survey_finish_state_text()
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    message.reply_text(text, reply_markup=keyboard_markup)
    context.user_data['state'] = botStates.SURVEY_FINISH_STATE
    return botStates.SURVEY_FINISH_STATE