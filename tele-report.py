import sys
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram_token import TOKEN, API_ID
import sqlite3
import subprocess

updater = Updater(TOKEN,
                  use_context=True)

# scraping = subprocess.Popen([sys.executable, "main.py"], shell=True)


def report(update: Update, context: CallbackContext):
    con = sqlite3.connect('ships_test.db')
    cur = con.cursor()
    cur.execute("SELECT Count(*) FROM LRS_details")
    db_length = cur.fetchall()[0][0]
    report_text = f"DB length: {db_length}"
    update.message.reply_text(report_text)
    con.close()


# def run_app(update: Update, context: CallbackContext):
#     global scraping
#     scraping = subprocess.Popen([sys.executable, "main.py"], shell=True)
#     update.message.reply_text("Script runs.")


def kill_app(update: Update, context: CallbackContext):
    global scraping
    scraping.kill()
    update.message.reply_text("Script has been stopped.")
    print("Script has been stopped.")


updater.dispatcher.add_handler(CommandHandler('report', report))
# updater.dispatcher.add_handler(CommandHandler('run', run_app))
updater.dispatcher.add_handler(CommandHandler('stop', kill_app))
# api_id = API_ID
# token = TOKEN
# message = "Working..."
updater.start_polling()
