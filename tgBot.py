import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
# from telegram.ext import MessageHandler, Filters


class tgBot():
    def __init__(self, token, startWord, helpWord):
        self.token     = token
        self.startWord = startWord
        self.helpWord  = helpWord

        # ----
        self.pairs = []
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher

    # -------------------------------
    def start_command(self, update, context):
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=self.startWord,
            parse_mode=telegram.ParseMode.MARKDOWN
        )
    # -------------------------------
    def help_command(self, update, context):
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=self.helpWord,
            parse_mode=telegram.ParseMode.MARKDOWN
        )
    # -------------------------------
    def basicCommands(self):
        # command
        # basic - start and help
        basics = [
            ["start", self.start_command],
            ["help",  self.help_command ],
        ]

        for c in basics:
            self.pairs.append(c)
    # -------------------------------
    def advancedCommands(self):
        pass
    # -------------------------------
    def addCommands(self):
        self.commands  = [item[0] for item in self.pairs]
        self.functions = [item[1] for item in self.pairs]
        # schedule commands
        for (co, fu) in zip(self.commands, self.functions):
            handler = CommandHandler(co,fu)
            self.dispatcher.add_handler(handler)
    # -------------------------------

    def run(self):
        self.basicCommands()
        self.advancedCommands()
        self.addCommands()
        
        self.updater.start_polling()
