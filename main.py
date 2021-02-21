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
import botStates, botHandlers

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
            MessageHandler(Filters.regex('[Нн]ет'), botHandlers.part_1_end_handler),
            MessageHandler(Filters.regex('[Дд]а'), botHandlers.part_1_question_2_handler),
            CommandHandler('start', botHandlers.start_state_handler),
        ],
        botStates.PART_1_QUESTION_2_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text, botHandlers.part_1_question_3_handler),
        ],
        botStates.PART_1_QUESTION_3_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text, botHandlers.survey_finish_handler),
        ],
        botStates.PART_1_END_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text, botHandlers.survey_finish_handler),
        ],
        # РАЗДЕЛ 2
        botStates.PART_2_QUESTION_1_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text, botHandlers.part_2_question_2_handler),
        ],
        botStates.PART_2_QUESTION_2_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text, botHandlers.part_2_question_3_handler),
        ],
        botStates.PART_2_QUESTION_3_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text, botHandlers.part_2_question_4_handler),
        ],
        botStates.PART_2_QUESTION_4_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text, botHandlers.part_2_question_5_handler),
        ],
        botStates.PART_2_QUESTION_5_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text, botHandlers.part_2_question_6_handler),
        ],
        botStates.PART_2_QUESTION_6_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text, botHandlers.part_2_question_7_handler),
        ],
        botStates.PART_2_QUESTION_7_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text, botHandlers.survey_finish_handler),
        ],

        # ОКОНЧАНИЕ
        botStates.SURVEY_FINISH_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.regex('[Нн]ет'), botHandlers.total_finish_handler),
            MessageHandler(Filters.regex('[Дд]а'), botHandlers.plans_info_handler),
        ],
        botStates.PLANS_INFO_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text, botHandlers.total_finish_handler),
        ],
        botStates.TOTAL_FINISH_STATE: [
            CommandHandler('start', botHandlers.start_state_handler),
            MessageHandler(Filters.text, botHandlers.total_finish_handler),
        ],

    },
    fallbacks=[CommandHandler('cancel', cancel)],

)

dispatcher.add_handler(conversation_handler)
updater.start_polling()
updater.idle()