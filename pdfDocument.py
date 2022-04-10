from PyPDF4 import PdfFileReader, PdfFileMerger
from pdf2image import convert_from_path

import os, glob, subprocess, shutil, platform
from os.path import splitext, basename, dirname

from loguru import logger
from tqdm import tqdm


digital_number = 3    # for image and pdf, digital number

# a PDF is a PdfDocument Object
# 


class PdfDocument():
    def __init__(self,
        fileName,
        startPage=1,
        endPage  =1, 
        columns  =2, 
        pageDividerPercent=65,
        pageColumnPercents=49, 
        k2dpi = 500,
        twoSides=False):

    
        self.path = str(fileName)
        self.startPage   = int(startPage)
        self.endPage     = int(endPage)

        # self.dilation  = int(dilation)

        self.columns            = int(columns)
        self.pageDividerPercent = pageDividerPercent   # divider, percent for one element
        self.pageColumnPercents = pageColumnPercents   # a list

        self.twoSides = twoSides
        self.k2dpi = k2dpi

        # output folders
        self.fileFolder     = (self.path).replace('.pdf', '')
        self.originalFolder = os.path.join(self.fileFolder,'original')
        # self.croppedFolder  = os.path.join(self.fileFolder,'cropped')
        self.pagepdfFolder  = os.path.join(self.fileFolder,'pagepdf' )
        self.pagepdfFigureFolder = os.path.join(self.fileFolder,'pagepdf', 'f' )
        self.pagepdfTableFolder  = os.path.join(self.fileFolder,'pagepdf', 'b' )

        self.xkfile  = (self.path).replace('.pdf', '_xk.pdf')
        self.fkfile  = (self.path).replace('.pdf', '_fk.pdf')
        self.bkfile  = (self.path).replace('.pdf', '_bk.pdf')
        self.bmfile  = (self.path).replace('.pdf', '_b.pdf')
        self.xmfile  = (self.path).replace('.pdf', '_x.pdf')
        self.fmfile  = (self.path).replace('.pdf', '_f.pdf')
        self.boxfile = (self.path).replace('.pdf', '_box.pdf')
        self.anntfile= (self.path).replace('.pdf', '_annt.pdf')

        self.finalFiles = [
            self.xkfile,
            self.xmfile,
            self.fkfile,
            self.fmfile,
            self.bkfile,
            self.bmfile,
            self.boxfile,
            self.anntfile,
        ]

        # log file
        self.logPath = (self.path).replace('.pdf', '.md')

        # parameters
        self.originalImagePaths = []

        self.metadata()

        # make sure no fake pages
        if (self.endPage > self.pdfPageNo):
            self.endPage = self.pdfPageNo

        self.createFolders()

    ######  metadata
    def metadata(self):
        print('PDF Name -- {}'.format(self.path) )

        inFile = open(self.path, "rb")
        self.inputPDF = PdfFileReader(inFile, strict=True)
        self.pdfPageNo = self.inputPDF.getNumPages()
        inFile.close()

        logger.success('{} -- Page number  recognized by code'.format(self.pdfPageNo) )

        # print('Block parameter = {}'.format(self.dilation) )
        logger.debug('Page coloumn(s) = {}'.format(self.columns) )
        logger.debug('Page divider percent = {}'.format(self.pageDividerPercent) )
        logger.debug('Page column percents = {}'.format(self.pageColumnPercents) )
    # ------------------------
    def createFolders(self):
        parentFolder = self.fileFolder

        if not os.path.exists(parentFolder):
            os.makedirs(parentFolder)
            
            # create folders
        for folder in ['original','cut','pagepdf' ]:
            childFolder = os.path.join(parentFolder,folder)
            if not os.path.exists(childFolder):
                os.makedirs(childFolder)
            
        for folder in ["f","b"]:
            childFolder = os.path.join(parentFolder,'pagepdf', folder)
            if not os.path.exists(childFolder):
                os.makedirs(childFolder)

        logger.info( "pagepdf folders created" )

    def createLog(self):
        pass

    def removeFiles(self):
            # delete pdf folder
        print("\nremove the pdf folder and its contents\n")
        shutil.rmtree(self.fileFolder)
        for fl in self.finalFiles:
            try:
                os.remove(fl)
                print(f"{fl} has been deleted!")
            except:
                print(f"No {fl}, skipping...")
    # ----------------------
    def convert2Image(self):
        print( '{0} pages will be processed in this session...\n'.format(self.endPage - self.startPage +1 ) )

        # read pdf and convert to images
        for i in tqdm( range( self.startPage-1, self.endPage ), desc="converting into images..." ):
            page = convert_from_path(self.path, first_page= i + 1 , last_page = i + 1)
            imagePath = '{0}.png'.format( str(i+1).zfill(digital_number) )
            originalImagePath = os.path.join( self.originalFolder, imagePath  )
            page[0].save(originalImagePath)            # save pdf page as image
            self.originalImagePaths.append(originalImagePath)
    # ----------------------
    def mergeAndReflow(self):
        dpi = self.k2dpi

        fileName, file_extension = splitext(self.path)
        textFolder = os.path.join(fileName,"pagepdf" )
        figFolder  = os.path.join(textFolder,"f")
        tableFolder= os.path.join(textFolder,"b")

        if os.path.exists(figFolder):
            for (folder,fileAdd, k2para) in zip(
                [figFolder,textFolder,tableFolder],
                ["_f.pdf", "_x.pdf","_b.pdf"], 
                ["-bpc 8 -c", "-bpc 1", "-bpc 1"] ):

                logger.debug(folder)

                # merge
                pdfs = glob.glob( os.path.join( folder,"*.pdf") )
                if len(pdfs) >0:
                    # merge
                    mergePDFs(pdfs)

                    # copy
                    mged = glob.glob( os.path.join( folder,"*_mg.pdf") )[0]
                    logger.info(mged)
                    destination = fileName + fileAdd
                    logger.info(destination)
                    shutil.move(mged, destination)
                    
                    # k2pdfopt reflow
                    file = os.path.join(".", destination)
                    fullCommand = 'k2pdfopt -x -dev kp3 -idpi {0} -odpi {1} -fc- -j 0 -col 1 -rt 0 {2} {3}'.format(dpi, dpi, k2para, file)

                    SysName = platform.system()
                    logger.debug(SysName)

                    if (SysName == 'Darwin') or (SysName=="Linux"):
                        fullCommand = 'echo "\n" | ' + fullCommand

                    print("the following command will be implemented:\n" + fullCommand + "\n")
                    subprocess.call(fullCommand, shell=True)

                    # rename
                    k2ed = destination.replace(".pdf","_k2opt.pdf")
                    os.rename(k2ed, k2ed.replace("_k2opt.pdf", "k.pdf") )

# --------------------
def mergePDFs(pdfs):
    merger = PdfFileMerger()

    pdfs.sort()
    filename, file_extension = splitext(pdfs[0])
    pdf_out = filename + '_mg' + file_extension

    for i in tqdm( range( len(pdfs) ), desc="merging pdfs..." ):
        merger.append(open(pdfs[i], 'rb'))

    with open(pdf_out, 'wb') as fout:
        merger.write(fout)
    
    merger.close()


"""            for (folder,fileAdd, k2para) in zip(
                [textFolder],
                ["_x.pdf"],
                ["-bpc 1"] ):"""
