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
import botStates, botHandlers, botPart1Handlers, botPart2Handlers, botPart3Handlers, botPart4Handlers

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

options = OptionsParser.parse()
updater = Updater(options.telegram_bot_token)
dispatcher = updater.dispatcher

def cancel(update: Update, context: CallbackContext) -> int:
    pass

conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', botHandlers.start_state_handler)],
    states={
        botStates.START_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.regex('Начнем'), botHandlers.question_1_handler),
        ],
        botStates.QUESTION_1_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text, botHandlers.question_2_handler),
        ],
        botStates.QUESTION_2_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text, botHandlers.fork_handler),
        ],
        botStates.FORK_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text, botHandlers.fork_handler),
        ],

        # РАЗДЕЛ 1
        botStates.PART_1_QUESTION_1_STATE: [
            MessageHandler(Filters.regex('[Нн]ет'), botPart1Handlers.part_1_question_4_handler),
            MessageHandler(Filters.regex('[Дд]а'), botPart1Handlers.part_1_question_2_handler),
            CommandHandler('start', botHandlers.start_state_handler),
        ],
        botStates.PART_1_QUESTION_2_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart1Handlers.part_1_question_3_handler),
        ],
        botStates.PART_1_QUESTION_3_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart1Handlers.part_1_survey_finish_handler),
        ],
        botStates.PART_1_QUESTION_4_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart1Handlers.part_1_survey_finish_handler),
        ],

        # РАЗДЕЛ 2
        botStates.PART_2_QUESTION_1_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart2Handlers.part_2_question_2_handler),
        ],
        botStates.PART_2_QUESTION_2_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart2Handlers.part_2_question_3_handler),
        ],
        botStates.PART_2_QUESTION_3_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart2Handlers.part_2_question_4_handler),
        ],
        botStates.PART_2_QUESTION_4_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart2Handlers.part_2_question_5_handler),
        ],
        botStates.PART_2_QUESTION_5_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart2Handlers.part_2_question_6_handler),
        ],
        botStates.PART_2_QUESTION_6_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart2Handlers.part_2_question_7_handler),
        ],
        botStates.PART_2_QUESTION_7_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart2Handlers.part_2_survey_finish_handler),
        ],

        # РАЗДЕЛ 3
        botStates.PART_3_QUESTION_1_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart3Handlers.part_3_question_2_handler),
        ],
        botStates.PART_3_QUESTION_2_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart3Handlers.part_3_question_3_handler),
        ],
        botStates.PART_3_QUESTION_3_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart3Handlers.part_3_question_4_handler),
        ],
        botStates.PART_3_QUESTION_4_STATE: [
            MessageHandler(Filters.regex('[Нн]ет'), botPart3Handlers.part_3_question_5_handler),
            MessageHandler(Filters.regex('[Дд]а'), botPart3Handlers.part_3_question_4_1_handler),
            CommandHandler('start', botHandlers.start_state_handler),
        ],
        botStates.PART_3_QUESTION_4_1_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart3Handlers.part_3_question_4_2_handler),
        ],
        botStates.PART_3_QUESTION_4_2_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart3Handlers.part_3_question_4_3_handler),
        ],
        botStates.PART_3_QUESTION_4_3_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart3Handlers.part_3_question_5_handler),
        ],
        botStates.PART_3_QUESTION_5_STATE: [
            MessageHandler(Filters.regex('[Нн]ет'), botPart3Handlers.part_3_question_6_handler),
            MessageHandler(Filters.regex('[Дд]а'), botPart3Handlers.part_3_question_5_1_handler),
            CommandHandler('start', botHandlers.start_state_handler),
        ],
        botStates.PART_3_QUESTION_5_1_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart3Handlers.part_3_question_5_2_handler),
        ],
        botStates.PART_3_QUESTION_5_2_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart3Handlers.part_3_question_5_3_handler),
        ],
        botStates.PART_3_QUESTION_5_3_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart3Handlers.part_3_question_6_handler),
        ],
        botStates.PART_3_QUESTION_6_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart3Handlers.part_3_survey_finish_handler),
        ],

        # РАЗДЕЛ 4
        botStates.PART_4_QUESTION_1_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart4Handlers.part_4_question_2_handler),
        ],
        botStates.PART_4_QUESTION_2_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart4Handlers.part_4_question_3_handler),
        ],
        botStates.PART_4_QUESTION_3_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart4Handlers.part_4_question_4_handler),
        ],
        botStates.PART_4_QUESTION_4_STATE: [
            MessageHandler(Filters.regex('[Нн]ет'), botPart4Handlers.part_4_question_5_handler),
            MessageHandler(Filters.regex('[Дд]а'), botPart4Handlers.part_4_question_4_1_handler),
            CommandHandler('start', botHandlers.start_state_handler),
        ],
        botStates.PART_4_QUESTION_4_1_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart4Handlers.part_4_question_4_2_handler),
        ],
        botStates.PART_4_QUESTION_4_2_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart4Handlers.part_4_question_5_handler),
        ],
        botStates.PART_4_QUESTION_5_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart4Handlers.part_4_question_6_handler),
        ],
        botStates.PART_4_QUESTION_6_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart4Handlers.part_4_question_7_handler),
        ],
        botStates.PART_4_QUESTION_7_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart4Handlers.part_4_question_8_handler),
        ],
        botStates.PART_4_QUESTION_8_STATE: [
            MessageHandler(Filters.regex('[Нн]ет'), botPart4Handlers.part_4_question_8_no_1_handler),
            MessageHandler(Filters.regex('[Дд]а'), botPart4Handlers.part_4_question_8_yes_1_handler),
            CommandHandler('start', botHandlers.start_state_handler),
        ],
        botStates.PART_4_QUESTION_8_NO_1_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart4Handlers.part_4_question_9_handler),
        ],
        botStates.PART_4_QUESTION_8_YES_1_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart4Handlers.part_4_question_9_handler),
        ],
        botStates.PART_4_QUESTION_9_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart4Handlers.part_4_question_10_handler),
        ],
        botStates.PART_4_QUESTION_10_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart4Handlers.part_4_question_11_handler),
        ],
        botStates.PART_4_QUESTION_11_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botPart4Handlers.part_4_question_12_handler),
        ],
        botStates.PART_4_QUESTION_12_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botHandlers.survey_finish_handler),
        ],

        # ОКОНЧАНИЕ
        botStates.SURVEY_FINISH_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.regex('[Нн]ет'), botHandlers.total_finish_handler),
            MessageHandler(Filters.regex('[Дд]а'), botHandlers.plans_info_handler),
        ],
        botStates.PLANS_INFO_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botHandlers.total_finish_handler),
        ],
        botStates.TOTAL_FINISH_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text | Filters.voice, botHandlers.total_finish_handler),
        ],
    },
    fallbacks=[CommandHandler('cancel', cancel)],

)

dispatcher.add_handler(conversation_handler)
updater.start_polling()
updater.idle()