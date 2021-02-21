import logging
from telegram import InlineQueryResult, InlineQueryResultArticle, ParseMode, InputTextMessageContent, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CallbackContext,
    InlineQueryHandler
)
import botMessageProvider
import botStates
import helpers

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start_state_handler(update: Update, context: CallbackContext) -> int:
    text = botMessageProvider.get_start_state_text()
    reply_keyboard = [['Начнем']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard)
    update.message.reply_text(text, reply_markup=keyboard_markup)
    return botStates.START_STATE


def question_1_handler(update: Update, context: CallbackContext) -> int:
    text = botMessageProvider.get_question_1_state_text()
    reply_keyboard = [['1', '2'], ['3', 'Больше трех']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard)
    update.message.reply_text(text, reply_markup=keyboard_markup)
    return botStates.QUESTION_1_STATE


def question_2_handler(update: Update, context: CallbackContext) -> int:
    def parse_answer(answer):
        language_count, success = helpers.intTryParse(answer)
        if not success:
            answer_mapping = {'1': 1, '2': 2, '3': 3, 'Больше трех': 4}
            language_count = answer_mapping.get(answer, -1)
        return language_count

    language_count = parse_answer(update.message.text)
    if language_count == -1:
        return botStates.QUESTION_1_STATE

    context.user_data['language_count'] = language_count

    text = botMessageProvider.get_question_2_state_text()
    reply_keyboard = [['Нет, не изучаю', 'Да, изучаю']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard)
    update.message.reply_text(text, reply_markup=keyboard_markup)
    return botStates.QUESTION_2_STATE


def fork_handler(update: Update, context: CallbackContext) -> int:
    language_count = context.user_data['language_count']
    answer = update.message.text.lower()
    if 'нет' in answer:
        if language_count == 1:
            # Раздел 1
            return part_1_question_1_handler(update, context)
        else:
            # Раздел 3
            return part_3_question_1_handler(update, context)
    elif 'да' in answer:
        if language_count == 1:
            # Раздел 2
            return part_2_question_1_handler(update, context)
        else:
            # Раздел 4
            return part_4_question_1_handler(update, context)
    else:
        return botStates.QUESTION_2_STATE


def part_1_question_1_handler(update: Update, context: CallbackContext) -> int:
    text = botMessageProvider.get_part_1_question_1_state_text()
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard)
    update.message.reply_text(text, reply_markup=keyboard_markup)
    return botStates.FORK_STATE


def part_2_question_1_handler(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Для чего учите новый язык?')
    return botStates.FORK_STATE


def part_3_question_1_handler(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Какие инструменты использовали для запоминания новых слов?')
    return botStates.FORK_STATE


def part_4_question_1_handler(update: Update, context: CallbackContext) -> int:
    # TODO: а кнопка "свой вариант ответа" где? и как сделать?
    reply_keyboard = [['Английский', 'Немецкий', 'Нидерландский',
                      'Французский', 'Итальянский', 'Португальский', 'Испанский']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard)
    update.message.reply_text('Какой язык сейчас учите?', reply_markup=keyboard_markup)
    return botStates.FORK_STATE
