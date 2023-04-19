from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove, Update,
    InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    CommandHandler, CallbackContext,
    ConversationHandler, MessageHandler,
    filters, Updater, CallbackQueryHandler,
    ContextTypes
)
from config import (
    API_KEY,
    API_SECRET,
    FAUNA_KEY,
    CLOUD_NAME
)
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from faunadb import query as q
from faunadb.client import FaunaClient
from faunadb.errors import NotFound
from flight_raccoon.flight_raccoon import give_me_flights, give_me_accomodation
import logging, datetime, pytz
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# configure cloudinary
cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET
)

# fauna client config
client = FaunaClient(secret=FAUNA_KEY)

# Define Options
BOT_START, BOT_CONFIG, BOT_REPLY, UNSET = range(4)
options = {
    'flights': give_me_flights,
    'accomodation': give_me_accomodation,
}

async def start(update, context: CallbackContext) -> int:
    bot = context.bot
    chat_id = update.message.chat.id
    await bot.send_message(
        chat_id=chat_id,
        text= "Hello! You are about to make your life easier."
        "Please choose the appropriate crawler and info you would like to scrape for."
    )
    reply_keyboard = [
        [
            InlineKeyboardButton(
                text="Flight Tickets",
                callback_data="flights"
            ),
            # InlineKeyboardButton(
            #     text="Accomodation",
            #     callback_data="accomodation"
            # )
        ]
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    await bot.send_message(
        chat_id=chat_id,
        text="Please choose what should I search for:",
        reply_markup=markup
    )
    return BOT_START

async def bot_start(update, context: CallbackContext) -> int: 
    bot = context.bot
    chat_id = update.callback_query.message.chat.id
    source_type = update.callback_query.data.lower()
    await bot.send_message(
        chat_id=chat_id,
        text=f"looking for {source_type} \n",
    )
    reply_keyboard = [
        [
            InlineKeyboardButton(
                text="Search",
                callback_data="search"
            )
        ]
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    await bot.send_message(
        chat_id=chat_id,
        text="Initiated search...",
        reply_markup=markup
    )
    # function to execute
    context.user_data['source'] = options[source_type]
    # type to print
    context.user_data['source_type'] = source_type
    return BOT_CONFIG

async def bot_config(update, context: CallbackContext) -> int: 
    bot = context.bot
    chat_id = update.callback_query.message.chat.id
    if (context.user_data['source_type'] == "flights"):
        await bot.send_message(
            chat_id=chat_id,
            text="Add the StartFrom(DD/MM/YYYY), Add the StartTo(DD/MM/YYYY), AirportFrom, AirportTo, MaxPrice, NightsLow, NightsBig, MaxDuration"
            "separated by commas(,)"
        )
    else:
        await bot.send_message(
            chat_id=chat_id,
            text="Add the StartFrom(DD/MM/YYYY), Add the StartTo(DD/MM/YYYY), Hotel, Apparts, MaxPrice, NightsLow, NightsBig"
            "separated by commas(,)"
        )
    return BOT_CONFIG

async def bot_reply(update: Update, context: CallbackContext) -> int:
    bot = context.bot
    chat_id = update.message.chat.id
    data = {
        'data': update.message.text,
        'user_data': context.user_data
    }
    context.job_queue.run_daily(bot_ping, datetime.time(hour=6, minute=27, tzinfo=pytz.timezone('Asia/Kolkata')),  days=(0, 1, 2, 3, 4, 5, 6), chat_id=chat_id, name=str(chat_id), data=data)
    await bot.send_message(
        chat_id=chat_id,
        text="Job started... Please wait for the next itteration of results..."
    )
    return ConversationHandler.END

async def bot_ping(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    try:
        result = job.data.get('user_data').get('source')(job.data.get('data'))
        if len(result) == 0:
            await context.bot.send_message(
                chat_id=job.chat_id,
                text=f"Sorry, I couldn't find anything for {job.data.get('data')}"
            )
        for v in result:
            await context.bot.send_message(
                chat_id=job.chat_id,
                text=v,
            )
    except Exception as e:
        logger.warning(e)

def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

async def cancel(update: Update, context: CallbackContext) -> int: 
    await update.message.reply_text(
        'Bye! I hope we can talk again some day.',
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Timer successfully cancelled!" if job_removed else "You have no active timer."
    await update.message.reply_text(text)
