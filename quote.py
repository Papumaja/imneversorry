from telegram import Update
from telegram.ext import CallbackContext
import random

import db

class Quote:
    def __init__(self):
        self.commands = { 'addq': self.addQuote,
                        'quote': self.getQuote,
                        'quotes': self.quotesCountHandler }

    def getCommands(self):
        return self.commands

    async def addQuote(self, update: Update, context: CallbackContext):
        if len(context.args) < 2:
            await context.bot.sendMessage(chat_id=update.message.chat.id, text='Usage: /addq <quotee> <quote>')
        else:
            quotee = context.args[0].strip('@')
            quote = ' '.join(context.args[1:])
            if quote[0] == '"' and quote[len(quote) - 1] == '"':
                quote = quote[1:len(quote) - 1]
            db.insertQuote(quote, quotee, update.message.chat.id, update.message.from_user.username)

    async def quotesCountHandler(self, update: Update, context: CallbackContext):
        if len(context.args) == 0:
            count = db.countQuotes(update.message.chat.id)
        else:
            quotee = context.args[0].strip('@')
            quotes = db.findQuotes(update.message.chat.id, quotee)
            count = len(quotes)

        await context.bot.sendMessage(chat_id=update.message.chat.id, text=str(count) + ' quotes')

    async def getQuote(self, update: Update, context: CallbackContext):
        if len(context.args) == 0:
            quotes = db.findQuotes(update.message.chat.id)
        else:
            quotee = context.args[0].strip('@')
            quotes = db.findQuotes(update.message.chat.id, quotee)
        quote = random.sample(quotes, 1)[0] or ("Imneversorry", "tapan kaikki")

        formated_quote = '"{}" - {}'.format(*quote)
        await context.bot.sendMessage(chat_id=update.message.chat.id, text=formated_quote)
