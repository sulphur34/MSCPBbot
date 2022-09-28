#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

import inspect
import logging

from telegram import __version__ as TG_VER
from pprint import pprint
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
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

START_ROUTES, END_ROUTES = range(2)
ONE, TWO, THREE = range(3)
request_list = {}


def write_param(update, param_name):
    request_id = f'ch{update.effective_chat.id}us{update.effective_user.id}msg{update.callback_query.message.id}'
    if request_id in request_list:
        request_list[request_id][param_name] = update.callback_query.data
    else:
        request_list[request_id] = {}
        request_list[request_id][param_name] = update.callback_query.data
    pass


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("Coversation started with ", user.first_name)
    keyboard = [
        [
            InlineKeyboardButton(text="Составить договор", callback_data=str(ONE)),
        ],
        [
            InlineKeyboardButton(text="Пояснение по замечаниям", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Здравствуйте. Выберите задачу", reply_markup=reply_markup)
    return START_ROUTES


async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    logger.info(query.data, 'chat', update.effective_chat.id, 'user', update.effective_user.id, 'message',
                update.callback_query.message.id,
                'update', update.update_id, inspect.currentframe().f_code.co_name)
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
    if query.data == 'new_request':
        await update.effective_message.reply_text("Здравствуйте. Выберите задачу", reply_markup=reply_markup)
        return START_ROUTES
    await query.edit_message_text(text="Здравствуйте. Выберите задачу", reply_markup=reply_markup)
    return START_ROUTES


async def contract_subject(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    logger.info(query.data, 'chat', update.effective_chat.id, 'user', update.effective_user.id, 'message',
                update.callback_query.message.id,
                'update', update.update_id, inspect.currentframe().f_code.co_name)
    await query.answer()
    # request_list['request_id'] = update.update_id
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
    query = update.callback_query
    logger.info("Contract type ", query)
    logger.info(query.data, 'chat', update.effective_chat.id, 'user', update.effective_user.id, 'message',
                update.callback_query.message.id,
                'update', update.update_id, inspect.currentframe().f_code.co_name)
    write_param(update, 'contract_subject')
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
    query = update.callback_query
    write_param(update, 'contract_type')
    logger.info(query.data, 'chat', update.effective_chat.id, 'user', update.effective_user.id, 'message',
                update.callback_query.message.id,
                'update', update.update_id, inspect.currentframe().f_code.co_name)
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
    query = update.callback_query
    write_param(update, 'counterpart_type')
    logger.info(query.data, 'chat', update.effective_chat.id, 'user', update.effective_user.id, 'message',
                update.callback_query.message.id,
                'update', update.update_id, inspect.currentframe().f_code.co_name)
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
    query = update.callback_query
    write_param(update, 'payment_system')
    logger.info(query.data, 'chat', update.effective_chat.id, 'user', update.effective_user.id, 'message',
                update.callback_query.message.id,
                'update', update.update_id, inspect.currentframe().f_code.co_name)
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
    query = update.callback_query
    write_param(update, 'edo_presence')
    logger.info(query.data, 'chat', update.effective_chat.id, 'user', update.effective_user.id, 'message',
                update.callback_query.message.id,
                'update', update.update_id, inspect.currentframe().f_code.co_name)
    pprint(request_list)
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(text="Продолжить работу", callback_data='new_request'),
        ],
        [
            InlineKeyboardButton(text="Завершить работу", callback_data=str(TWO)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Ссылка на договор", reply_markup=reply_markup)
    return END_ROUTES


async def repeat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    logger.info(query.data, 'chat', update.effective_chat.id, 'user', update.effective_user.id, 'message',
                update.callback_query.message.id,
                'update', update.update_id, inspect.currentframe().f_code.co_name)
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(text="Продолжить работу", callback_data=str(THREE)),
        ],
        [
            InlineKeyboardButton(text="Завершить работу", callback_data=str(TWO)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Хотите продолжить работу?", reply_markup=reply_markup)
    return END_ROUTES


async def explanations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    logger.info(query.data, 'chat', update.effective_chat.id, 'user', update.effective_user.id, 'message',
                update.callback_query.message.id,
                'update', update.update_id, inspect.currentframe().f_code.co_name)
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
    query = update.callback_query
    logger.info(query.data, 'chat', update.effective_chat.id, 'user', update.effective_user.id, 'message',
                update.callback_query.message.id,
                'update', update.update_id, inspect.currentframe().f_code.co_name)
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(text="Продолжить работу", callback_data='new_request'),
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
    query = update.callback_query
    logger.info(query.data, 'chat', update.effective_chat.id, 'user', update.effective_user.id, 'message',
                update.callback_query.message.id,
                'update', update.update_id, inspect.currentframe().f_code.co_name)
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(text="Продолжить работу", callback_data='new_request'),
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
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Спасибо за использование нашего бота. Для повторного запуска напишите - /start")
    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token("5730170263:AAEtXblg63a2XWYkv3cc2NzmAlwWBRn2yPE").build()
    bot = Bot
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
                CallbackQueryHandler(start_over, pattern="^" + 'new_request' + "$"),
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
