#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from options import Options
from optionsParser import OptionsParser
from telegram import InlineQueryResult, InlineQueryResultArticle, ParseMode, InputTextMessageContent, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    InlineQueryHandler
)
from telegram.utils.helpers import escape_markdown
import states, commonHandlers, part1Handlers, part2Handlers, part3Handlers, part4Handlers

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

options = OptionsParser.parse()
#TODO: обработка --help_mode

updater = Updater(options.telegram_bot_token)
dispatcher = updater.dispatcher

def admin_state_handler(update: Update, context: CallbackContext) -> int:
    return commonHandlers.admin_state_handler(update, context, options.admin_ids)

conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', commonHandlers.start_state_handler),
    ],
    states={
        states.START_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            CommandHandler('admin', admin_state_handler),
            MessageHandler(Filters.regex('Начнем'), commonHandlers.question_1_handler),
        ],
        states.QUESTION_1_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text, commonHandlers.question_2_handler),
        ],
        states.QUESTION_2_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text, commonHandlers.fork_handler),
        ],
        states.FORK_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text, commonHandlers.fork_handler),
        ],

        # РАЗДЕЛ 1
        states.PART_1_QUESTION_1_STATE: [
            MessageHandler(Filters.regex('[Нн]ет'), part1Handlers.part_1_question_4_handler),
            MessageHandler(Filters.regex('[Дд]а'), part1Handlers.part_1_question_2_handler),
            CommandHandler('start', commonHandlers.start_state_handler),
        ],
        states.PART_1_QUESTION_2_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part1Handlers.part_1_question_3_handler),
        ],
        states.PART_1_QUESTION_3_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part1Handlers.part_1_survey_finish_handler),
        ],
        states.PART_1_QUESTION_4_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part1Handlers.part_1_survey_finish_handler),
        ],

        # РАЗДЕЛ 2
        states.PART_2_QUESTION_1_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part2Handlers.part_2_question_2_handler),
        ],
        states.PART_2_QUESTION_2_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part2Handlers.part_2_question_3_handler),
        ],
        states.PART_2_QUESTION_3_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part2Handlers.part_2_question_4_handler),
        ],
        states.PART_2_QUESTION_4_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part2Handlers.part_2_question_5_handler),
        ],
        states.PART_2_QUESTION_5_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part2Handlers.part_2_question_6_handler),
        ],
        states.PART_2_QUESTION_6_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part2Handlers.part_2_question_7_handler),
        ],
        states.PART_2_QUESTION_7_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part2Handlers.part_2_survey_finish_handler),
        ],

        # РАЗДЕЛ 3
        states.PART_3_QUESTION_1_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part3Handlers.part_3_question_2_handler),
        ],
        states.PART_3_QUESTION_2_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part3Handlers.part_3_question_3_handler),
        ],
        states.PART_3_QUESTION_3_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part3Handlers.part_3_question_4_handler),
        ],
        states.PART_3_QUESTION_4_STATE: [
            MessageHandler(Filters.regex('[Нн]ет'), part3Handlers.part_3_question_5_handler),
            MessageHandler(Filters.regex('[Дд]а'), part3Handlers.part_3_question_4_1_handler),
            CommandHandler('start', commonHandlers.start_state_handler),
        ],
        states.PART_3_QUESTION_4_1_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part3Handlers.part_3_question_4_2_handler),
        ],
        states.PART_3_QUESTION_4_2_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part3Handlers.part_3_question_4_3_handler),
        ],
        states.PART_3_QUESTION_4_3_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part3Handlers.part_3_question_5_handler),
        ],
        states.PART_3_QUESTION_5_STATE: [
            MessageHandler(Filters.regex('[Нн]ет'), part3Handlers.part_3_question_6_handler),
            MessageHandler(Filters.regex('[Дд]а'), part3Handlers.part_3_question_5_1_handler),
            CommandHandler('start', commonHandlers.start_state_handler),
        ],
        states.PART_3_QUESTION_5_1_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part3Handlers.part_3_question_5_2_handler),
        ],
        states.PART_3_QUESTION_5_2_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part3Handlers.part_3_question_5_3_handler),
        ],
        states.PART_3_QUESTION_5_3_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part3Handlers.part_3_question_6_handler),
        ],
        states.PART_3_QUESTION_6_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part3Handlers.part_3_survey_finish_handler),
        ],

        # РАЗДЕЛ 4
        states.PART_4_QUESTION_1_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part4Handlers.part_4_question_2_handler),
        ],
        states.PART_4_QUESTION_2_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part4Handlers.part_4_question_3_handler),
        ],
        states.PART_4_QUESTION_3_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part4Handlers.part_4_question_4_handler),
        ],
        states.PART_4_QUESTION_4_STATE: [
            MessageHandler(Filters.regex('[Нн]ет'), part4Handlers.part_4_question_5_handler),
            MessageHandler(Filters.regex('[Дд]а'), part4Handlers.part_4_question_4_1_handler),
            CommandHandler('start', commonHandlers.start_state_handler),
        ],
        states.PART_4_QUESTION_4_1_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part4Handlers.part_4_question_4_2_handler),
        ],
        states.PART_4_QUESTION_4_2_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part4Handlers.part_4_question_5_handler),
        ],
        states.PART_4_QUESTION_5_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part4Handlers.part_4_question_6_handler),
        ],
        states.PART_4_QUESTION_6_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part4Handlers.part_4_question_7_handler),
        ],
        states.PART_4_QUESTION_7_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part4Handlers.part_4_question_8_handler),
        ],
        states.PART_4_QUESTION_8_STATE: [
            MessageHandler(Filters.regex('[Нн]ет'), part4Handlers.part_4_question_8_no_1_handler),
            MessageHandler(Filters.regex('[Дд]а'), part4Handlers.part_4_question_8_yes_1_handler),
            CommandHandler('start', commonHandlers.start_state_handler),
        ],
        states.PART_4_QUESTION_8_NO_1_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part4Handlers.part_4_question_9_handler),
        ],
        states.PART_4_QUESTION_8_YES_1_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part4Handlers.part_4_question_9_handler),
        ],
        states.PART_4_QUESTION_9_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part4Handlers.part_4_question_10_handler),
        ],
        states.PART_4_QUESTION_10_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part4Handlers.part_4_question_11_handler),
        ],
        states.PART_4_QUESTION_11_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, part4Handlers.part_4_question_12_handler),
        ],
        states.PART_4_QUESTION_12_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, commonHandlers.survey_finish_handler),
        ],

        # ОКОНЧАНИЕ
        states.SURVEY_FINISH_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.regex('[Нн]ет'), commonHandlers.total_finish_handler),
            MessageHandler(Filters.regex('[Дд]а'), commonHandlers.plans_info_handler),
        ],
        states.PLANS_INFO_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, commonHandlers.total_finish_handler),
        ],
        states.TOTAL_FINISH_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, commonHandlers.total_finish_handler),
        ],

        # АДМИН
        states.ADMIN_STATE: [
            CommandHandler('start', commonHandlers.start_state_handler),
            CommandHandler('list', commonHandlers.admin_get_answers_list_handler),
            CommandHandler('export', commonHandlers.admin_export_state_handler),
            MessageHandler(Filters.regex('Получить список проголосовавших'), commonHandlers.admin_get_answers_list_handler),
            MessageHandler(Filters.regex('Экспорт результатов в HTML'), commonHandlers.admin_export_state_handler),
        ],
        states.ADMIN_EXPORT_RESULT_STATE: [
            MessageHandler(Filters.regex('Вернуться в главное меню админки'), admin_state_handler),
        ],
        states.ADMIN_USERNAME_LIST_STATE: [
            MessageHandler(Filters.regex('Вернуться в главное меню админки'), admin_state_handler),
        ],
    },
    fallbacks=[CommandHandler('cancel', commonHandlers.cancel)],
)

dispatcher.add_handler(conversation_handler)
updater.start_polling()
updater.idle()
