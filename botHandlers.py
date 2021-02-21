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

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start_state_handler(update: Update, context: CallbackContext) -> int:
    # TODO: проверить, проходил ли юзер раньше этот опрос. если проходил то надо предупредить что ответы перезапишутся

    text = botMessageProvider.get_start_state_text()
    reply_keyboard = [['Начнем']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text, reply_markup=keyboard_markup)
    return botStates.START_STATE


def survey_finish_handler(update: Update, context: CallbackContext) -> int:
    text = botMessageProvider.get_survey_finish_state_text()
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text, reply_markup=keyboard_markup)
    return botStates.SURVEY_FINISH_STATE


def plans_info_handler(update: Update, context: CallbackContext) -> int:
    text = botMessageProvider.get_plans_info_state_text()
    update.message.reply_text(text, parse_mode='Markdown')
    return botStates.PLANS_INFO_STATE


def total_finish_handler(update: Update, context: CallbackContext) -> int:
    text = 'Теперь точно всё :) Спасибо и до скорых встреч!'
    update.message.reply_text(text)
    return botStates.TOTAL_FINISH_STATE


def question_1_handler(update: Update, context: CallbackContext) -> int:
    text = botMessageProvider.get_question_1_state_text()
    reply_keyboard = [['1', '2'], ['3', 'Больше трех']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
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
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
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

# РАЗДЕЛ 1
def part_1_question_1_handler(update: Update, context: CallbackContext) -> int:
    text = botMessageProvider.get_part_1_question_1_state_text()
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text, reply_markup=keyboard_markup)
    return botStates.PART_1_QUESTION_1_STATE


def part_1_question_2_handler(update: Update, context: CallbackContext) -> int:
    text = 'Где *ищете перевод* иностранного слова?'
    update.message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_1_QUESTION_2_STATE


def part_1_question_3_handler(update: Update, context: CallbackContext) -> int:
    text = 'Бывает так что правильное значение не найти сразу? Как убеждаетесь в правильном смысле?'
    update.message.reply_text(text)
    return botStates.PART_1_QUESTION_3_STATE


def part_1_end_handler(update: Update, context: CallbackContext) -> int:
    text = 'Эх, тогда вопросов больше нет :) Расскажите вообще что думаете про изучение иностранных языков?'
    update.message.reply_text(text)
    return botStates.PART_1_END_STATE


# РАЗДЕЛ 2
def part_2_question_1_handler(update: Update, context: CallbackContext) -> int:
    text = '*Для чего* учите новый язык?'
    update.message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_2_QUESTION_1_STATE


def part_2_question_2_handler(update: Update, context: CallbackContext) -> int:
    text = 'Как *ищете перевод* иностранного слова?'
    update.message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_2_QUESTION_2_STATE


def part_2_question_3_handler(update: Update, context: CallbackContext) -> int:
    text = 'Какие *инструменты* используете для запоминания новых слов?'
    update.message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_2_QUESTION_3_STATE


def part_2_question_4_handler(update: Update, context: CallbackContext) -> int:
    text = 'Бывают *проблемы с поиском* правильного смысла перевода?'
    update.message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_2_QUESTION_4_STATE


def part_2_question_5_handler(update: Update, context: CallbackContext) -> int:
    text = 'Насколько вам важна *эффективность* процесса изучения языка?'
    update.message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_2_QUESTION_5_STATE


def part_2_question_6_handler(update: Update, context: CallbackContext) -> int:
    text = 'Как отслеживаете свой *текущий прогресс* в изучении нового языка?'
    update.message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_2_QUESTION_6_STATE


def part_2_question_7_handler(update: Update, context: CallbackContext) -> int:
    text = 'Что вас *мотивирует* изучать новый язык?'
    update.message.reply_text(text, parse_mode='Markdown')
    return botStates.PART_2_QUESTION_7_STATE


# РАЗДЕЛ 3
def part_3_question_1_handler(update: Update, context: CallbackContext) -> int:
    text = 'Какие инструменты использовали для запоминания новых слов?'
    update.message.reply_text(text)
    return botStates.FORK_STATE


# РАЗДЕЛ 4
def part_4_question_1_handler(update: Update, context: CallbackContext) -> int:
    # TODO: а кнопка "свой вариант ответа" где? и как сделать?
    text = 'Какой язык сейчас учите?'
    reply_keyboard = [['Английский', 'Немецкий', 'Нидерландский',
                       'Французский', 'Итальянский', 'Португальский', 'Испанский']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text, reply_markup=keyboard_markup)
    return botStates.FORK_STATE
