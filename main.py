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
            MessageHandler(Filters.regex('Начнем'), botHandlers.question_1_handler),
        ],
        botStates.QUESTION_1_STATE: [
            MessageHandler(Filters.text, botHandlers.question_2_handler),
            CommandHandler('cancel', cancel)
        ],
        botStates.QUESTION_2_STATE: [
            MessageHandler(Filters.text, botHandlers.fork_handler),
            CommandHandler('cancel', cancel)
        ],
        botStates.FORK_STATE: [
            MessageHandler(Filters.text, botHandlers.fork_handler),
            CommandHandler('cancel', cancel)
        ],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

dispatcher.add_handler(conversation_handler)
updater.start_polling()
updater.idle()