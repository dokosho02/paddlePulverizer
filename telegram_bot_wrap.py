import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
# from telegram import Document

# import schedule
import time, platform, datetime, os, sys
import subprocess

from loguru import logger
import shutil

from tgBot import tgBot

################################

# pulverizerFile = "pulverizer.py"

token = os.environ["PULVERIZER_BOT_TOKEN"]
startWord = """I'm ready to work.\nYou can use `/help` command to learn how to use me."""
helpWord = """
        I am a page layout analysis bot (for pdf document - reading on Kindle Paperwhite 3 device).
        If you want to remove all your data, just type `/rm`.
        If you have any questions, please contact `@hk_tobeno1`,
        or visit the [website](https://github.com/dokosho02/paddlePulverizer).
        """
# "I'm a dictionary bot.\n\n\tIf you have any questions, please contact @hk\\_tobeno1."
# def getpdfName(pdfFilename, file_path):
#     if pdfFilename=="":
#         pdfFilename = file_path
#     return pdfFilename
################################
def get_platform():
    SysName = platform.system()
    return SysName

################################
def run_python_script(pyFile):

    pyEngine = 'python3'    # default for MacOS
    SysName = get_platform()
    if (SysName=='Windows'):    # Windows
        pyEngine = 'python'
    elif (SysName=='Darwin'):    # MacOS
        pyEngine = 'python3'
    
    pyShell = f"{pyEngine} {pyFile}"
    subprocess.call(pyShell, shell=True)
################################

class PulverizerBot(tgBot):
    def __init__(self, token, startWord, helpWord):
        super().__init__(token, startWord, helpWord)
        # self.token = os.environ['PULVERIZER_BOT_TOKEN']

        self.botDowloadFolder = "bot"
        self.pulverizerFile = "pulverizer.py"
        self.workFolder = ""

        # core
        self.currentPdfPath = ""
    ################################
    def file_identification(self, update, context):
        # create folder
        self.workFolder = os.path.join(self.botDowloadFolder, str(update.message.chat_id) )
        if not os.path.exists(self.botDowloadFolder):
            os.makedirs(self.botDowloadFolder)

        if not os.path.exists(self.workFolder):
                os.makedirs(self.workFolder)
        ## bot geting the document and its file_name
        doc = context.bot.get_file(update.message.document.file_id)
        fileName = update.message.document.file_name
        print(fileName)
        file_path = os.path.join( self.workFolder, fileName)

        ##bot saving this file to a directory on your PC
        doc.download(file_path)

        file_mame, file_extension = os.path.splitext(file_path)
        if file_extension== ".pdf":
            self.currentPdfPath=file_path
        elif file_extension== ".md":
            self.mdPath =file_path
        update.message.reply_text(text=f"You have sent me a {file_extension} file." )
    ################################################################
    def rename_pdf(self, update, context):
        self.workFolder = os.path.join(self.botDowloadFolder, str(update.message.chat_id) )

        convert_parameter = ' '.join(context.args)
        print(convert_parameter)
        if convert_parameter!=None:
            self.new_pdfPath = os.path.join( self.workFolder, f"{convert_parameter}.pdf")

            try:
                os.rename(self.currentPdfPath, self.new_pdfPath)
                self.currentPdfPath = self.new_pdfPath
            except:
                pass
    ################################################################
    def plas(self, update, context):
        self.workFolder = os.path.join(self.botDowloadFolder, str(update.message.chat_id) )

        convert_parameter = ' '.join(context.args)
        print(convert_parameter)
        if convert_parameter!=None:
            run_python_script( f"{self.pulverizerFile} {self.currentPdfPath} {convert_parameter}" )
        update.message.reply_text(text="Page layout analysis - complete!")
    # ------------
    def send_box_md_files(self, update, context):        
        self.mdPath = self.currentPdfPath.replace('.pdf', '.md')
        box_pdfname = self.currentPdfPath.replace('.pdf', '_box.pdf')
        
        context.bot.send_document(chat_id=update.message.chat_id, document=open(self.mdPath, 'rb') )
        context.bot.send_document(chat_id=update.message.chat_id, document=open(box_pdfname, 'rb') )
    ################################################################
    def md_crop(self, update, context):
        self.workFolder = os.path.join(self.botDowloadFolder, str(update.message.chat_id) )

        convert_parameter = ' '.join(context.args)
        print(convert_parameter)
        if convert_parameter!=None:
            run_python_script( f"{self.pulverizerFile} {self.currentPdfPath} -md {convert_parameter}" )

        annotate_pdfname = self.currentPdfPath.replace('.pdf', '_annt.pdf')
        context.bot.send_document(chat_id=update.message.chat_id, document=open(annotate_pdfname, 'rb') )
    ################################################################
    def xk_file(self, update, context):
        self.workFolder = os.path.join(self.botDowloadFolder, str(update.message.chat_id) )

        xk_filepath = self.currentPdfPath.replace(".pdf", "_xk.pdf")
        context.bot.send_document(chat_id=update.message.chat_id, document=open(xk_filepath, 'rb') )
    ################################################################
    def rm_files(self, update, context):
        self.workFolder = os.path.join(self.botDowloadFolder, str(update.message.chat_id) )

        shutil.rmtree(self.workFolder)
        update.message.reply_text( text="All your data is deleted!" )
        self.currentPdfPath=""
    ################################################################
    def list_files(self, update, context):
        self.workFolder = os.path.join(self.botDowloadFolder, str(update.message.chat_id) )

        finalText = ""
        try:
            dir_list = os.listdir(self.workFolder)
            for i in dir_list:
                finalText+=f"{i}\n"
            finalText = f"{len(dir_list)} file(s) in your folder:\n" + finalText
        except:
            finalText = "Nothing..."
        # finalText = ""
        # [finalText=finalText+f"{i}n" for i in dir_list]
        update.message.reply_text( text=finalText )
    ################################################################
    def send_files(self, update, context):
        self.workFolder = os.path.join(self.botDowloadFolder, str(update.message.chat_id) )

        convert_parameter = ' '.join(context.args)
        print(convert_parameter)
        if convert_parameter!=None:
            files = convert_parameter.split(" ")

            for fl in files:
                file_to_send = os.path.join(self.workFolder, fl)
                context.bot.send_document(chat_id=update.message.chat_id, document=open(file_to_send, 'rb') )

    def setCurrentPdf(self,update, context):
        self.workFolder = os.path.join(self.botDowloadFolder, str(update.message.chat_id) )

        convert_parameter = ' '.join(context.args)
        print(convert_parameter)
        if convert_parameter!=None:
            self.currentPdfPath = os.path.join( self.workFolder, f"{convert_parameter}.pdf")
    
    def getCurrentPdf(self,update, context):
        self.workFolder = os.path.join(self.botDowloadFolder, str(update.message.chat_id) )
        update.message.reply_text( text=self.currentPdfPath )

################################

    def advancedCommands(self):
    
        # download
        download_handler = MessageHandler(Filters.document, self.file_identification)
        self.dispatcher.add_handler(download_handler)

        adv =[
            ["pl", self.plas],    # core
            ["md", self.md_crop],
            ["xk", self.xk_file],
            ["pp", self.send_box_md_files],
            ["gp", self.getCurrentPdf],    # settings
            ["sp", self.setCurrentPdf],
            ["rn", self.rename_pdf],       # file
            ["rm", self.rm_files],
            ["ls", self.list_files],
            ["sn", self.send_files],
        ]

        for a in adv:
            self.pairs.append(a)


# --------------------------------------
def main():
    plvbot = PulverizerBot(token,startWord, helpWord)
    plvbot.run()
# --------------------------------------
if __name__ == '__main__':
    # --------------
    main()
    # --------------


# ---------------------
"""
https://stackoverflow.com/questions/65801985/not-able-to-save-the-file-in-custom-path-directory-using-python-telegram-bot
"""