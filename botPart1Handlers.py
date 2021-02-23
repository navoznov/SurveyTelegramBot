#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import ParseMode, InputTextMessageContent, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Message
from telegram.ext import (
    Updater,
    CallbackContext,
    ConversationHandler
)
import helpers
import botMessageProvider
import botStates
import answerHelper

# РАЗДЕЛ 1
def part_1_question_1_handler(update: Update, context: CallbackContext) -> int:
    context.user_data['part_number'] = 1

    keys = [f'question{i+1}' for i in range(4)]
    for key in keys:
        answerHelper.set_empty_answer(context.user_data, key)


    text = botMessageProvider.get_part_1_question_1_state_text()
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    helpers.get_message(update).reply_text(text, reply_markup=keyboard_markup)
    context.user_data['state'] = botStates.PART_1_QUESTION_1_STATE
    return botStates.PART_1_QUESTION_1_STATE


def part_1_question_2_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question1')
    text = 'Где *ищете перевод* иностранного слова?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_1_QUESTION_2_STATE


def part_1_question_3_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question2')
    text = 'Бывает так что правильное значение не найти сразу? Как убеждаетесь в правильном смысле?'
    message.reply_text(text)
    context.user_data['state'] = botStates.PART_1_QUESTION_3_STATE
    return botStates.PART_1_QUESTION_3_STATE


def part_1_question_4_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    answerHelper.save_answer(message, context, 'question1')

    text = 'Эх, тогда вопросов больше нет :) Расскажите вообще что думаете про изучение иностранных языков?'
    message.reply_text(text)
    context.user_data['state'] = botStates.PART_1_QUESTION_4_STATE
    return botStates.PART_1_QUESTION_4_STATE


def part_1_survey_finish_handler(update: Update, context: CallbackContext) -> int:
    message = helpers.get_message(update)
    if context.user_data['state'] == botStates.PART_1_QUESTION_3_STATE:
        answerHelper.save_answer(message, context, 'question3')
    else:
        answerHelper.save_answer(message, context, 'question4')

    text = botMessageProvider.get_survey_finish_state_text()
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    message.reply_text(text, reply_markup=keyboard_markup)
    context.user_data['state'] = botStates.SURVEY_FINISH_STATE
    return botStates.SURVEY_FINISH_STATE