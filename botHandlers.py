#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from telegram import InlineQueryResult, InlineQueryResultArticle, ParseMode, InputTextMessageContent, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Message
from telegram.ext import (
    Updater,
    CallbackContext,
    ConversationHandler
)
import botMessageProvider
import botStates
import helpers
import botAnswerSaver

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def _get_message(update: Update) -> Message:
    return update.message if update.message != None else update.edited_message

def start_state_handler(update: Update, context: CallbackContext) -> int:
    # TODO: проверить, проходил ли юзер раньше этот опрос. если проходил то надо предупредить что ответы перезапишутся

    text = botMessageProvider.get_start_state_text()
    reply_keyboard = [['Начнем']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    _get_message(update).reply_text(text, reply_markup=keyboard_markup)
    return botStates.START_STATE


def survey_finish_handler(update: Update, context: CallbackContext) -> int:
    text = botMessageProvider.get_survey_finish_state_text()
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    _get_message(update).reply_text(text, reply_markup=keyboard_markup)
    context.user_data['state'] = botStates.SURVEY_FINISH_STATE
    return botStates.SURVEY_FINISH_STATE


def plans_info_handler(update: Update, context: CallbackContext) -> int:
    text = botMessageProvider.get_plans_info_state_text()
    _get_message(update).reply_text(text, parse_mode='Markdown')
    context.user_data['state'] = botStates.PLANS_INFO_STATE
    return botStates.PLANS_INFO_STATE


def total_finish_handler(update: Update, context: CallbackContext) -> int:
    if context.user_data['state'] == botStates.PLANS_INFO_STATE:
        botAnswerSaver.save_answer(update.message, context.user_data, 'final1')
    else:
        botAnswerSaver.set_empty_answer(context.user_data, 'final1')

    botAnswerSaver.save_user_answers_to_file(update.effective_user, context.user_data)

    text = 'Теперь точно всё :) Спасибо и до скорых встреч!'
    _get_message(update).reply_text(text)
    return ConversationHandler.END


def question_1_handler(update: Update, context: CallbackContext) -> int:
    text = botMessageProvider.get_question_1_state_text()
    reply_keyboard = [['1', '2'], ['3', 'Больше трех']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    _get_message(update).reply_text(text, reply_markup=keyboard_markup)
    return botStates.QUESTION_1_STATE


def question_2_handler(update: Update, context: CallbackContext) -> int:
    def parse_answer(answer):
        language_count, success = helpers.intTryParse(answer)
        if not success:
            answer_mapping = {'1': 1, '2': 2, '3': 3, 'Больше трех': 4}
            language_count = answer_mapping.get(answer, -1)
        return language_count

    message = _get_message(update)
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
            return part_1_question_1_handler(update, context)
        else:
            # Раздел 3
            return part_3_question_1_handler(update, context)
    elif YES in answer:
        user_data['start2'] = YES

        if language_count == 1:
            # Раздел 2
            return part_2_question_1_handler(update, context)
        else:
            # Раздел 4
            return part_4_question_1_handler(update, context)
    else:
        return botStates.QUESTION_2_STATE

# РАЗДЕЛ 1
def part_1_question_1_handler(update: Update, context: CallbackContext) -> int:
    context.user_data['part_number'] = 1

    keys = [f'question{i+1}' for i in range(4)]
    for key in keys:
        botAnswerSaver.set_empty_answer(context.user_data, key)


    text = botMessageProvider.get_part_1_question_1_state_text()
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    _get_message(update).reply_text(text, reply_markup=keyboard_markup)
    context.user_data['state'] = botStates.PART_1_QUESTION_1_STATE
    return botStates.PART_1_QUESTION_1_STATE


def part_1_question_2_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question1')
    text = 'Где *ищете перевод* иностранного слова?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_1_QUESTION_2_STATE


def part_1_question_3_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question2')
    text = 'Бывает так что правильное значение не найти сразу? Как убеждаетесь в правильном смысле?'
    message.reply_text(text)
    context.user_data['state'] = botStates.PART_1_QUESTION_3_STATE
    return botStates.PART_1_QUESTION_3_STATE


def part_1_question_4_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question1')

    text = 'Эх, тогда вопросов больше нет :) Расскажите вообще что думаете про изучение иностранных языков?'
    message.reply_text(text)
    context.user_data['state'] = botStates.PART_1_QUESTION_4_STATE
    return botStates.PART_1_QUESTION_4_STATE


def part_1_survey_finish_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    if context.user_data['state'] == botStates.PART_1_QUESTION_3_STATE:
        botAnswerSaver.save_answer(message, context.user_data, 'question3')
    else:
        botAnswerSaver.save_answer(message, context.user_data, 'question4')

    text = botMessageProvider.get_survey_finish_state_text()
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    message.reply_text(text, reply_markup=keyboard_markup)
    context.user_data['state'] = botStates.SURVEY_FINISH_STATE
    return botStates.SURVEY_FINISH_STATE


# РАЗДЕЛ 2
def part_2_question_1_handler(update: Update, context: CallbackContext) -> int:
    context.user_data['part_number'] = 2

    keys = [f'question{i+1}' for i in range(7)]
    for key in keys:
        botAnswerSaver.set_empty_answer(context.user_data, key)

    text = '*Для чего* учите новый язык?'
    _get_message(update).reply_text(text, parse_mode='Markdown')
    return botStates.PART_2_QUESTION_1_STATE


def part_2_question_2_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question1')
    text = 'Как *ищете перевод* иностранного слова?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_2_QUESTION_2_STATE


def part_2_question_3_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question2')
    text = 'Какие *инструменты* используете для запоминания новых слов?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_2_QUESTION_3_STATE


def part_2_question_4_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question3')
    text = 'Бывают *проблемы с поиском* правильного смысла перевода?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_2_QUESTION_4_STATE


def part_2_question_5_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question4')
    text = 'Насколько вам важна *эффективность* процесса изучения языка?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_2_QUESTION_5_STATE


def part_2_question_6_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question5')
    text = 'Как отслеживаете свой *текущий прогресс* в изучении нового языка?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_2_QUESTION_6_STATE


def part_2_question_7_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question6')
    text = 'Что вас *мотивирует* изучать новый язык?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_2_QUESTION_7_STATE


def part_2_survey_finish_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question7')
    text = botMessageProvider.get_survey_finish_state_text()
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    message.reply_text(text, reply_markup=keyboard_markup)
    context.user_data['state'] = botStates.SURVEY_FINISH_STATE
    return botStates.SURVEY_FINISH_STATE

# РАЗДЕЛ 3
def part_3_question_1_handler(update: Update, context: CallbackContext) -> int:
    context.user_data['part_number'] = 3

    keys = [f'question{i+1}' for i in range(7)]
    for key in keys:
        botAnswerSaver.set_empty_answer(context.user_data, key)

    text = 'Какие инструменты использовали для запоминания новых слов?'
    _get_message(update).reply_text(text)
    return botStates.PART_3_QUESTION_1_STATE


def part_3_question_2_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question1')
    text = 'Как искали перевод иностранного слова?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_3_QUESTION_2_STATE


def part_3_question_3_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question2')
    text = 'Бывали проблемы с поиском правильного смысла перевода? Как находили верный перевод?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_3_QUESTION_3_STATE


def part_3_question_4_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question3')
    text = 'Когда-нибудь проверяли сколько вы знаете слов?'
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    message.reply_text(text, reply_markup=keyboard_markup)
    context.user_data['state'] = botStates.PART_3_QUESTION_4_STATE
    return botStates.PART_3_QUESTION_4_STATE


def part_3_question_4_1_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question4')
    text = 'Сколько примерно слов сейчас знаете?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_3_QUESTION_4_1_STATE


def part_3_question_4_2_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question4_1')
    text = 'Чем пользовались чтобы узнать это число?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_3_QUESTION_4_2_STATE


def part_3_question_4_3_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question4_2')
    text = 'Продолжаете набирать словарный запас?'
    message.reply_text(text, parse_mode='Markdown')
    context.user_data['state'] = botStates.PART_3_QUESTION_4_3_STATE
    return botStates.PART_3_QUESTION_4_3_STATE


def part_3_question_5_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    if context.user_data['state'] = botStates.PART_3_QUESTION_4_3_STATE:
        botAnswerSaver.save_answer(message, context.user_data, 'question4_3')
    elif context.user_data['state'] = botStates.PART_3_QUESTION_4_STATE:
        botAnswerSaver.save_answer(message, context.user_data, 'question4')

    text = 'Планируете изучать новый язык?'
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    message.reply_text(text, reply_markup=keyboard_markup)
    context.user_data['state'] = botStates.PART_3_QUESTION_5_STATE
    return botStates.PART_3_QUESTION_5_STATE


def part_3_question_5_1_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question5')
    text = 'Что вас останавливает?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_3_QUESTION_5_1_STATE


def part_3_question_5_2_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question5_1')
    text = 'Как думаете, вам поможет знание двух языков в изучении третьего? Если да, то чем?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_3_QUESTION_5_2_STATE


def part_3_question_5_3_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question5_2')
    text = 'С чего начнёте учить новый язык?'
    message.reply_text(text, parse_mode='Markdown')
    context.user_data['state'] = botStates.PART_3_QUESTION_5_3_STATE
    return botStates.PART_3_QUESTION_5_3_STATE


def part_3_question_6_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    if context.user_data['state'] = botStates.PART_3_QUESTION_5_3_STATE:
        botAnswerSaver.save_answer(message, context.user_data, 'question5_3')
    elif context.user_data['state'] = botStates.PART_3_QUESTION_5_STATE:
        botAnswerSaver.save_answer(message, context.user_data, 'question5')

    text = 'Какой мотивации не хватает чтобы начать изучать новый язык?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_3_QUESTION_6_STATE


def part_3_survey_finish_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question6')
    text = botMessageProvider.get_survey_finish_state_text()
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    message.reply_text(text, reply_markup=keyboard_markup)
    context.user_data['state'] = botStates.SURVEY_FINISH_STATE
    return botStates.SURVEY_FINISH_STATE


# РАЗДЕЛ 4
def part_4_question_1_handler(update: Update, context: CallbackContext) -> int:
    context.user_data['part_number'] = 4

    # TODO: а кнопка "свой вариант ответа" где? и как сделать?
    text = 'Какой язык сейчас учите?'
    reply_keyboard = [['Английский', 'Немецкий', 'Нидерландский',
                       'Французский', 'Итальянский', 'Португальский', 'Испанский']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    _get_message(update).reply_text(text, reply_markup=keyboard_markup)
    return botStates.PART_4_QUESTION_1_STATE


def part_4_question_2_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question6')
    text = '*Для чего* учите еще один новый язык?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_4_QUESTION_2_STATE


def part_4_question_3_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question6')
    text = 'Как *ищете перевод* иностранного слова'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_4_QUESTION_3_STATE


def part_4_question_4_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question6')
    text = 'Бывают *проблемы с поиском* правильного смысла перевода?'
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    message.reply_text(text, parse_mode='Markdown', reply_markup=keyboard_markup)
    return botStates.PART_4_QUESTION_4_STATE


def part_4_question_4_1_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question6')
    text = 'Как находили правильный перевод?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_4_QUESTION_4_1_STATE


def part_4_question_4_2_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question6')
    text = 'Что помогает найти правильный смысл слова?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_4_QUESTION_4_2_STATE


def part_4_question_5_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question6')
    text = 'Какие методики используете чтобы запоминать новые слова'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_4_QUESTION_5_STATE


def part_4_question_6_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question6')
    text = 'Какие еще *инструменты* используете для изучения языка'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_4_QUESTION_6_STATE


def part_4_question_7_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question6')
    text = 'Как *знание* других языков и *опыт* их изучения *помогает* с новым языком'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_4_QUESTION_7_STATE


def part_4_question_8_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question6')
    text = 'Проверяете ли значение нового слова в переводе на известные вам языки?'
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    message.reply_text(text, reply_markup=keyboard_markup)
    return botStates.PART_4_QUESTION_8_STATE


def part_4_question_8_yes_1_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question6')
    text = 'Чем полезно проверять перевод нового слова сразу на несколько языков?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_4_QUESTION_8_YES_1_STATE


def part_4_question_8_no_1_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question6')
    text = 'Как узнаете смысл слова? Переводите обычно на свой родной язык или как-то иначе?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_4_QUESTION_8_NO_1_STATE


def part_4_question_9_handler(update: Update, context: CallbackContext) -> int:
    # сюда переход с двух состояний (8yes и 8no) - это надо как то обработать наверное
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question6')
    text = 'Насколько вам важна *эффективность* процесса изучения языка?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_4_QUESTION_9_STATE


def part_4_question_10_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question6')
    text = 'Как отслеживаете свой *текущий уровень* в изучении нового языка?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_4_QUESTION_10_STATE


def part_4_question_11_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question6')
    text = 'Отслеживаете текущее количество известных слов? Если да, то как?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_4_QUESTION_11_STATE


def part_4_question_12_handler(update: Update, context: CallbackContext) -> int:
    message = _get_message(update)
    botAnswerSaver.save_answer(message, context.user_data, 'question6')
    text = 'Что вас *мотивирует* изучать новый язык?'
    message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_4_QUESTION_12_STATE












