from telegram import Update
from telegram.ext import CallbackContext
import re
import db
import random
import operator

class Tagaaja:
    def __init__(self):
        self.commands = { 'tag': self.addTagHandler,
                          'tagged': self.taggedSearchHandler,
                          'tags': self.tagTargetSearchHandler }

    def getCommands(self):
        return self.commands

    async def addTagHandler(self, update: Update, context: CallbackContext):
        args = context.args
        if len(args) < 2:
            await context.bot.sendMessage(chat_id=update.message.chat_id, text='Usage: /tag <asia> <tagi>')
            return

        target = args[0]
        tag = args[1]
        chat_id = update.message.chat.id
        db.upsertTag(tag, target, chat_id, update.message.from_user.username)

    async def taggedSearchHandler(self, update: Update, context: CallbackContext):
        args = context.args
        if len(args) < 1:
            await context.bot.sendMessage(chat_id=update.message.chat_id, text='Usage: /tagged <tagi>')
            return

        tag = args[0]
        chat_id = update.message.chat.id
        tagged_rows = db.findTagged(tag, chat_id)
        tagged = [row[0] for row in tagged_rows]
        await context.bot.sendMessage(chat_id=update.message.chat_id,
                        parse_mode='Markdown',
                        text='Tagged as \"*{}*\": \"{}\"'.format(tag, '\", \"'.join(tagged)))

    async def tagTargetSearchHandler(self, update: Update, context: CallbackContext):
        args = context.args
        if len(args) < 1:
            await context.bot.sendMessage(chat_id=update.message.chat_id, text='Usage: /tags <asia>')
            return

        target = args[0]
        chat_id = update.message.chat.id
        tags_rows = db.findTargetTags(target, chat_id)
        tags = [row[0] for row in tags_rows]
        await context.bot.sendMessage(chat_id=update.message.chat_id,
                        parse_mode='Markdown',
                        text='\"*{}*\": \"{}\"'.format(target, '\", \"'.join(tags)))
