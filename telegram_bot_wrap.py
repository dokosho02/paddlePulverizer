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


################################

# pulverizerFile = "pulverizer.py"



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

class PulverizerBot():
    def __init__(self):
        self.token = os.environ['PULVERIZER_BOT_TOKEN']
        self.botDowloadFolder = "bot"
        self.pulverizerFile = "pulverizer.py"
        self.workFolder = ""

        # core
        self.currentPdfPath = ""

    ################################
    def help_command(self, update, context):
        descrip = """
        I am a page layout analysis bot (for pdf document - reading on Kindle Paperwhite 3 device).
        If you want to remove all your data, just type `/rm`.
        If you have any questions, please contact `@hk_tobeno1`.
        """

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=descrip,
            parse_mode=telegram.ParseMode.MARKDOWN
            )
            # text="*bold* _italic_ `fixed width font` [link](http://google.com).", parse_mode=telegram.ParseMode.MARKDOWN
    ################################
    def start(self, update, context):
        self.workFolder = os.path.join(self.botDowloadFolder, str(update.message.chat_id) )
        context.bot.send_message(chat_id=update.message.chat_id, text="I'm ready to work.\nYou can use `/help` command to learn how to use me.", parse_mode=telegram.ParseMode.MARKDOWN)
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

    def startBot(self):
        updater = Updater(token=self.token, use_context=True)
        dispatcher = updater.dispatcher

        # command

        # basic - start and help
        start_handler = CommandHandler('start', self.start)
        dispatcher.add_handler(start_handler)

        help_handler = CommandHandler('help', self.help_command)
        dispatcher.add_handler(help_handler)

        # download
        download_handler = MessageHandler(Filters.document, self.file_identification)
        dispatcher.add_handler(download_handler)

        # functions
        # core
        pl_handler = CommandHandler('pl', self.plas)
        dispatcher.add_handler(pl_handler)

        md_handler = CommandHandler('md', self.md_crop)
        dispatcher.add_handler(md_handler)

        xk_handler = CommandHandler('xk', self.xk_file)
        dispatcher.add_handler(xk_handler)

        # file manipulation
        pp_handler = CommandHandler('pp', self.send_box_md_files)
        dispatcher.add_handler(pp_handler)
        gp_handler = CommandHandler('gp', self.getCurrentPdf)
        dispatcher.add_handler(gp_handler)
        sp_handler = CommandHandler('sp', self.setCurrentPdf)
        dispatcher.add_handler(sp_handler)

        rn_handler = CommandHandler('rn', self.rename_pdf)
        dispatcher.add_handler(rn_handler)
        rm_handler = CommandHandler('rm', self.rm_files)
        dispatcher.add_handler(rm_handler)
        ls_handler = CommandHandler('ls', self.list_files)
        dispatcher.add_handler(ls_handler)
        send_handler = CommandHandler('sn', self.send_files)
        dispatcher.add_handler(send_handler)
        # --------------
        updater.start_polling()

# --------------------------------------
def main():
    plvbot = PulverizerBot()
    plvbot.startBot()
# --------------------------------------
if __name__ == '__main__':
    # --------------
    main()
    # --------------


# ---------------------
"""
https://stackoverflow.com/questions/65801985/not-able-to-save-the-file-in-custom-path-directory-using-python-telegram-bot
"""