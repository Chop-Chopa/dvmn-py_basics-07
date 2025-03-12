from pytimeparse import parse
from dotenv import load_dotenv
import os
import ptbot


def reply(chat_id, text):
    secs_left = parse(text)
    message_id = bot.send_message(chat_id, "Осталось {} секунд!".format(secs_left))
    bot.create_countdown(secs_left, notify, chat_id=chat_id, message_id=message_id, total_time=secs_left)
    bot.create_timer(secs_left + 1, massage, chat_id=chat_id)


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify(secs_left, chat_id, message_id, total_time):
    progress = render_progressbar(total_time, total_time - secs_left)
    bot.update_message(chat_id, message_id, "Осталось {secs_left} секунд!\n{progress}".format(secs_left=secs_left, progress=progress))


def massage(chat_id):
    bot.send_message(chat_id, "Время вышло!")


def main():
    global bot, telegram_token, telegram_chat_id

    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    telegram_chat_id = os.getenv('TG_CHAT_ID')
    
    bot = ptbot.Bot(telegram_token)
    bot.reply_on_message(reply)
    bot.run_bot()


if __name__ == '__main__':
    main()
