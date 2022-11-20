from PyPDF4 import PdfFileReader, PdfFileMerger
from pdf2image import convert_from_path

import os, glob, subprocess, shutil, platform
from os.path import splitext, basename, dirname
import codecs

from loguru import logger
from tqdm import tqdm


from pdf_annotate import PdfAnnotator, Location, Appearance


from pdfPage import PdfPage
from pic2pdf import image_to_pdf


digital_number = 3    # for image and pdf, digital number

boxColors = [ (0,0,1), (1, 0, 0), (0,1,0)]    # BRG, x-b-f
thickness = 1

# a PDF is a PdfDocument Object
class PdfDocument():
    def __init__(self,
        fileName,
        startPage=1,
        endPage  =1,
        columns  =2,
        pageDividerPercent=65,
        pageColumnPercents=49, 
        k2dpi = 500,
        mdFile = None,
        twoSides=False):
  
        self.path        = str(fileName)
        self.startPage   = int(startPage)
        self.endPage     = int(endPage)

        # self.dilation  = int(dilation)

        self.columns            = int(columns)
        self.pageDividerPercent = pageDividerPercent   # divider, percent for one element
        self.pageColumnPercents = pageColumnPercents   # a list

        self.twoSides = twoSides
        self.k2dpi = k2dpi

        # log file
        self.mdFile = mdFile
        self.logPath = (self.path).replace('.pdf', '.md')
    # -----------------------------------------
    def run(self):
        self.metadata()

        # define all files
        self.allFiles()

        self.removeFiles()
        self.createFolders()

        if self.mdFile:
            self.cropByLog()
        else:
            # parameters
            self.originalImagePaths = []
            self.cropFromScratch()
    # -----------------------------------------
    def cropByLog(self):
        if ( os.path.exists(self.logPath) ):
            print("\na log file exists!\n")
            self.cropFromLog()
            self.mergeAndReflow()
            # finish
    # -----------------------------------------
    def cropFromLog(self):
        # self.removeFiles()
        # self.createFolders()

        # read log file
        f = codecs.open(doc.logPath,"r",encoding='utf-8')
        g = f.readlines()
        f.close()

        annotator = PdfAnnotator(self.path)

        startPage = int( (g[0].split())[0]) 
        endPage   = int( (g[-1].split())[0])
        
        pageAmount = endPage - startPage + 1
        print(f"{pageAmount} pages from log file information\n")

        with tqdm(total=pageAmount, desc="cropping...") as pbar:
            for i in range(pageAmount):
                singlePdfPage = PdfPage(self.path, i+startPage)    # back project to pdf page

                labelGroup = ["x", "b", "f"]
                count = 1
                for (bl, bc) in zip(labelGroup, boxColors):
                    areaInfo = []
                    for ln in g:
                        pageNo_str, blockType, xs, ys, xe, ye = ln.split()
                        page_ant = int(pageNo_str)-1
                        if ( page_ant == i+startPage-1) and (blockType==bl):
                            areas = [xs, ys, xe, ye]
                            for j in range( len(areas) ):
                                areas[j] = float(areas[j])
                            areaInfo.append(areas)

                            # annoatate
                            # square
                            annotator.add_annotation(
                                'square',
                                location = Location(
                                    x1=areas[0],
                                    y1=areas[1],
                                    x2=areas[2],
                                    y2=areas[3],
                                    page=page_ant
                                ),
                                appearance = Appearance(
                                    stroke_color=bc,
                                    stroke_width=thickness,
                                )
                            )

                            # text
                            annotator.add_annotation(
                                'text',
                                location = Location(
                                    x1=areas[0],
                                    y1=areas[1],
                                    x2=areas[2],
                                    y2=areas[3],
                                    page=page_ant
                                ),
                                appearance = Appearance(
                                    fill=(1,0,0),
                                    content=str(count),
                                    font_size=40
                                )
                            )
                            count += 1
                    singlePdfPage.cropBlocksByPixel(areaInfo, self.pagepdfFolder, bl)

                pbar.update(1)
        pbar.close()

        outpath_annotated = self.path.replace(".pdf", "_annt.pdf")
        annotator.write(outpath_annotated)

    # -----------------------------------------
    def cropFromScratch(self):
        # self.removeFiles()
        # self.createFolders()
        
        # create log file
        f = codecs.open(self.logPath,"w",encoding='utf-8')
        f.close()
    
        print("\nThere is no log file.\nStarting to cut the pdf document with plas (page layout analysis)...\n")

        self.convert2Image()
        with tqdm(total=len(self.originalImagePaths), desc="cutting with AI tech...") as pbar:
            for i in range(len(self.originalImagePaths)):
                self.processPage(i)
                pbar.update(1)
        
        pbar.close()
        # ----
        image_to_pdf(self.path)
    # -----------------------------------------
    def processPage(self, i):
        # start to process images
        from imagePage import ImagePage
        # image
        # 2 create an object of ImagePage
        pageNo = self.startPage + i - 1
        # pageNo = int( os.path.split(imgPage.path)[-1].strip(".png") )
        imgPage = ImagePage(self.originalImagePaths[i], pageNo+1)

        # 3 crop margins, no functions for paddleocr
        xylu = imgPage.cropMarginsbyPercents()    # x,y,l,u, new origin, point, here are 0,0

        imgPage.layoutAnalysisByPaddle( len(self.originalImagePaths)  )    # 4 page layout analysis -  cut! divide!
        imgPage.arrangeLayout(self.columns, self.pageDividerPercent, self.pageColumnPercents)    # 5 arrange layout
        imgPage.saveBlockImage()

        # pdf
        singlePdfPage = PdfPage(self.path, pageNo)    # back project to pdf page
        # calculate and cut
        infoGroup = [imgPage.textInfoOrdered, imgPage.tableInfoOrdered, imgPage.figureInfoOrdered ]
        labelGroup = ["x", "b", "f"]
        for (bi, bl) in zip( infoGroup, labelGroup):
            areaInfo = []
            # write to log file
            f = codecs.open(self.logPath,"a",encoding='utf-8')
            for xywh in bi:
                areas = singlePdfPage.calculatePDFCropArea(xylu,xywh)
                areaInfo.append( areas )
                f.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(pageNo+1, bl, areas[0],areas[1],areas[2],areas[3] ) )
            # page No - label - 
            singlePdfPage.cropBlocksByPixel(areaInfo, self.pagepdfFolder, bl)

            f.close()
    # ----------------------------------------
    def metadata(self):
        print(f'PDF Name -- {self.path}')

        # get page number
        inFile = open(self.path, "rb")
        self.inputPDF = PdfFileReader(inFile, strict=True)
        self.pdfPageNo = self.inputPDF.getNumPages()
        inFile.close()
        logger.success(f"{self.pdfPageNo} -- Page number  recognized by code" )

        # parameters
        # print('Block parameter = {}'.format(self.dilation) )
        logger.debug(f"Page coloumn(s) = {self.columns}")
        logger.debug(f"Page divider percent = {self.pageDividerPercent}")
        logger.debug(f"Page column percents = {self.pageColumnPercents}")

        # make sure no fake pages
        if (self.endPage > self.pdfPageNo):
            self.endPage = self.pdfPageNo

    # ---------------------------------------------------------------------------
    def allFiles(self):
        # definitions
        # output folders
        self.fileFolder     = (self.path).replace('.pdf', '')
        self.originalFolder = os.path.join(self.fileFolder,'original')
        # self.croppedFolder  = os.path.join(self.fileFolder,'cropped')

        self.pagepdfFolder       = os.path.join(self.fileFolder,'pagepdf')
        self.pagepdfFigureFolder = os.path.join(self.fileFolder,'pagepdf', 'f')
        self.pagepdfTableFolder  = os.path.join(self.fileFolder,'pagepdf', 'b')

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
    # ------------------------
    def createFolders(self):
        parentFolder = self.fileFolder

        if not os.path.exists(parentFolder):
            os.makedirs(parentFolder)
            
        # create folders
        for folder in ['original','cut','pagepdf']:
            childFolder = os.path.join(parentFolder,folder)
            if not os.path.exists(childFolder):
                os.makedirs(childFolder)
            
        for folder in ["f","b"]:
            childFolder = os.path.join(parentFolder,'pagepdf', folder)
            if not os.path.exists(childFolder):
                os.makedirs(childFolder)

        logger.info("pagepdf folders created")
    # ------------------------
    # def createLog(self):
    #     pass
    # ------------------------
    def removeFiles(self):
        # delete pdf folder
        try:
            print("\nremove the pdf folder and its contents\n")
            shutil.rmtree(self.fileFolder)
        except:
            print("No folders to remove, skipping...")
        
        # delete final output files
        for fl in self.finalFiles:
            try:
                os.remove(fl)
                print(f"{fl} has been deleted!")
            except:
                print(f"No {fl}, skipping...")
    # ----------------------
    def convert2Image(self):
        processedPageNo = self.endPage - self.startPage +1 
        print( f"{processedPageNo} pages will be processed in this session...\n" )

        # read pdf and convert to images
        for i in tqdm( range( self.startPage-1, self.endPage ), desc="converting into images..." ):
            page = convert_from_path(self.path, first_page= i + 1 , last_page = i + 1)
            imagePath = f"{str(i+1).zfill(digital_number)}.png"
            originalImagePath = os.path.join(self.originalFolder, imagePath)
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
                pdfs = glob.glob( os.path.join(folder, "*.pdf") )
                if len(pdfs)>0:
                    # merge
                    mergePDFs(pdfs)

                    # copy
                    mged = glob.glob( os.path.join( folder,"*_mg.pdf") )[0]
                    logger.info(mged)
                    destination = fileName + fileAdd
                    logger.info(destination)
                    shutil.move(mged, destination)
                    
                    # k2pdfopt reflow
                    reflowed = os.path.join(".", destination)
                    fullCommand = f"k2pdfopt -x -dev kp3 -idpi {dpi} -odpi {dpi} -fc- -j 0 -col 1 -rt 0 {k2para} {reflowed}"

                    SysName = platform.system()
                    logger.debug(SysName)

                    if (SysName == 'Darwin') or (SysName=="Linux"):
                        fullCommand = 'echo "\n" | ' + fullCommand

                    print(f"the following command will be implemented:\n{fullCommand}\n")
                    subprocess.call(fullCommand, shell=True)

                    # rename
                    k2ed = destination.replace(".pdf","_k2opt.pdf")
                    os.rename(k2ed, k2ed.replace("_k2opt.pdf", "k.pdf") )

# ----------------------------------------
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
