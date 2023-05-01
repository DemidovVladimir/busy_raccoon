from telegram import (
    ReplyKeyboardRemove, Update,
    InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    CallbackContext, ConversationHandler, ContextTypes
)
from flight_raccoon.flight_raccoon import give_me_flights, give_me_accomodation
from flight_raccoon.exceptions import InvalidArguments
import logging, datetime, pytz
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Define Options
BOT_START, BOT_SCHEDULER, BOT_SCHEDULER_SET, BOT_CONFIG, BOT_REPLY, UNSET = range(6)
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
                text="Configure scheduler",
                callback_data="scheduler"
            ),
        ]
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    await bot.send_message(
        chat_id=chat_id,
        text="Please choose what should I search for:",
        reply_markup=markup
    )
    return BOT_SCHEDULER

async def bot_scheduler(update, context: CallbackContext) -> int: 
    bot = context.bot
    chat_id = update.callback_query.message.chat.id
    await bot.send_message(
        chat_id=chat_id,
        text="Add scheduler parameters: time to get results from bot: hours:minutes, timezone"
        "separated by commas(,) example: 10:30, Europe/Berlin"
    )
    return BOT_SCHEDULER

async def bot_scheduler_set(update: Update, context: CallbackContext) -> int:
    bot = context.bot
    chat_id = update.message.chat.id
    data = update.message.text
    data = data.split(',')
    if len(data) > 1:
        data = [x.strip() for x in data]
        tz = data[0].split(':')
        if len(tz) > 1:
            tz = [x.strip() for x in tz]
            context.user_data['scheduler'] = {
                'hours': tz[0],
                'minutes': tz[1],
                'timezone': data[1]
            }
            hours, minutes, timezone = context.user_data['scheduler'].values()
            await update.message.reply_text(
                f"You will be notified by this bot every day at {hours}: {minutes}, using {timezone} timezone",
            )
            reply_keyboard = [
                [
                    InlineKeyboardButton(
                        text="Flight Tickets",
                        callback_data="flights"
                    )
                ]
            ]
            markup = InlineKeyboardMarkup(reply_keyboard)
            await bot.send_message(
                chat_id=chat_id,
                text="Please choose what should I search for:",
                reply_markup=markup
            )
            return BOT_CONFIG
        else:
            await update.message.reply_text(
                "Please provide arguments according instructions: time to get results from bot: hours:minutes, timezone",
            )
            return ConversationHandler.END
    else:
        await bot.send_message(
            chat_id=chat_id,
            text="Please provide arguments according instructions: time to get results from bot: hours:minutes, timezone",
            reply_markup=markup
        )
        return ConversationHandler.END

async def bot_config(update, context: CallbackContext) -> int: 
    source_type = update.callback_query.data.lower()
    context.user_data['source'] = options[source_type]
    context.user_data['source_type'] = source_type
    bot = context.bot
    chat_id = update.callback_query.message.chat.id
    await bot.send_message(
        chat_id=chat_id,
        text="Add the starting search date(DD/MM/YYYY), Add the ending search date(DD/MM/YYYY), Take of Airport, Destination Airport, Max Price, Min Nights in location, Max Nights in destination, Max Flight duration in hours"
        "separated by commas(,) example: 23/07/2023, 25/08/2023, BER, ALA, 600,  20, 30, 15"
    )
    return BOT_CONFIG

async def bot_reply(update: Update, context: CallbackContext) -> int:
    hours, minutes, timezone = context.user_data['scheduler'].values()
    bot = context.bot
    chat_id = update.message.chat.id
    data = {
        'data': update.message.text,
        'user_data': context.user_data
    }
    logger.info(context.user_data['scheduler'])
    try:
        context.job_queue.run_daily(bot_ping, datetime.time(hour=int(hours), minute=int(minutes), tzinfo=pytz.timezone(timezone)),  days=(0, 1, 2, 3, 4, 5, 6), chat_id=chat_id, name=str(chat_id), data=data)
        # context.job_queue.run_once(bot_ping, 15, chat_id=chat_id, name=str(chat_id), data=data)
        await bot.send_message(
            chat_id=chat_id,
            text="Job started... Please wait for the next itteration of results..."
        )
    except Exception as e:
        logger.warning(e)
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
    except InvalidArguments:
        logger.warning('Lack of arguments')

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

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)