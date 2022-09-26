#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""Simple inline keyboard bot with multiple CallbackQueryHandlers.
This Bot uses the Application class to handle the bot.
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""
import logging

from telegram import __version__ as TG_VER

from data import ContractData

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Stages
START_ROUTES, END_ROUTES = range(2)
# Callback data
ONE, TWO, THREE = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("Coversation started with ", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton(text="Составить договор", callback_data=str(ONE)),
        ],
        [
            InlineKeyboardButton(text="Пояснение по замечаниям", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await update.message.reply_text("Здравствуйте. Выберите задачу", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return START_ROUTES


async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(text="Составить договор", callback_data=str(ONE)),
        ],
        [
            InlineKeyboardButton(text="Пояснение по замечаниям", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    await query.edit_message_text(text="Здравствуйте. Выберите задачу", reply_markup=reply_markup)
    return START_ROUTES


async def contract_subject(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(text="Поставка", callback_data='supply'),
        ],
        [
            InlineKeyboardButton(text="Подряд", callback_data='subcontract'),
        ],
        [
            InlineKeyboardButton(text="Оказание услуг", callback_data='services'),
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data=str(THREE)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Выберите предмет договора", reply_markup=reply_markup)
    return 'contract_type'


async def contract_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    logger.info("Contract type ", query)
    print(query.data)
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(text="Доходный", callback_data='profit'),
        ],
        [
            InlineKeyboardButton(text="Расходный", callback_data='expenses'),
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data=str(THREE)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Выберите тип договора", reply_markup=reply_markup)
    return 'counterpart_type'


async def counterpart_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    print(query.data)
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(text="Плательщик НДС", callback_data='NDS'),
        ],
        [
            InlineKeyboardButton(text="Не платит НДС", callback_data='nonNDS'),
        ],
        [
            InlineKeyboardButton(text="Физическое лицо", callback_data='individual'),
        ],
        [
            InlineKeyboardButton(text="Неизвестен", callback_data='unknown'),
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data=str(THREE)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Выберите тип контрагента", reply_markup=reply_markup)
    return 'payment_system'


async def payment_system(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    print(query.data)
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(text="Предоплата", callback_data='prepay'),
        ],
        [
            InlineKeyboardButton(text="Постоплата", callback_data='postpay'),
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data=str(THREE)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Выберите систему оплаты", reply_markup=reply_markup)
    return 'edo_presence'


async def edo_presence(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    print(query.data)
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(text='ЭДО есть', callback_data='EDOpresent'),
        ],
        [
            InlineKeyboardButton(text="ЭДО нет", callback_data='EDOabsent'),
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data=str(THREE)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Укажите наличие ЭДО", reply_markup=reply_markup)
    return 'get_contract'


async def get_contract(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    print(query.data)
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(text="Продолжить работу", callback_data=str(ONE)),
        ],
        [
            InlineKeyboardButton(text="Завершить работу", callback_data=str(TWO)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Ссылка на договор", reply_markup=reply_markup)
    return END_ROUTES


async def repeat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    print(query.data)
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(text="Продолжить работу", callback_data=str(ONE)),
        ],
        [
            InlineKeyboardButton(text="Завершить работу", callback_data=str(TWO)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Хотите продолжить работу?", reply_markup=reply_markup)
    return END_ROUTES


async def explanations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    print(query.data)
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Перечень замечаний", callback_data='remarks_list'),
            InlineKeyboardButton("Комментарий эксперта", callback_data='expert_comment'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Выберите действие", reply_markup=reply_markup
    )
    return START_ROUTES


async def remarks_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    print(query.data)
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(text="Продолжить работу", callback_data=str(ONE)),
        ],
        [
            InlineKeyboardButton(text="Завершить работу", callback_data=str(TWO)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Список замечаний", reply_markup=reply_markup
    )
    return END_ROUTES


async def expert_comment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    print(query.data)
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(text="Продолжить работу", callback_data=str(ONE)),
        ],
        [
            InlineKeyboardButton(text="Завершить работу", callback_data=str(TWO)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Переход к общению с экспертом", reply_markup=reply_markup
    )
    return END_ROUTES


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Спасибо за использование нашего бота. Для повторного запуска напишите - /start")
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5730170263:AAEtXblg63a2XWYkv3cc2NzmAlwWBRn2yPE").build()

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(contract_subject, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(explanations, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(repeat, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(remarks_list, pattern="^" + 'remarks_list' + "$"),
                CallbackQueryHandler(expert_comment, pattern="^" + 'expert_comment' + "$"),
            ],
            'contract_type': [
                CallbackQueryHandler(repeat, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(contract_type, pattern="^" + 'supply' + "$"),
                CallbackQueryHandler(contract_type, pattern="^" + 'subcontract' + "$"),
                CallbackQueryHandler(contract_type, pattern="^" + 'services' + "$"),
            ],
            'counterpart_type': [
                CallbackQueryHandler(repeat, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(counterpart_type, pattern="^" + 'profit' + "$"),
                CallbackQueryHandler(counterpart_type, pattern="^" + 'expenses' + "$"),
            ],
            'payment_system': [
                CallbackQueryHandler(repeat, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(payment_system, pattern="^" + 'NDS' + "$"),
                CallbackQueryHandler(payment_system, pattern="^" + 'nonNDS' + "$"),
                CallbackQueryHandler(payment_system, pattern="^" + 'individual' + "$"),
                CallbackQueryHandler(payment_system, pattern="^" + 'unknown' + "$"),
            ],
            'edo_presence': [
                CallbackQueryHandler(repeat, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(edo_presence, pattern="^" + 'prepay' + "$"),
                CallbackQueryHandler(edo_presence, pattern="^" + 'postpay' + "$"),
            ],
            'get_contract': [
                CallbackQueryHandler(repeat, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(get_contract, pattern="^" + 'EDOpresent' + "$"),
                CallbackQueryHandler(get_contract, pattern="^" + 'EDOabsent' + "$"),
            ],
            END_ROUTES: [
                CallbackQueryHandler(start_over, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(end, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(end, pattern="^" + str(THREE) + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
