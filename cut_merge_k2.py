from tqdm import tqdm
import datetime, os, codecs
import shutil

# customize
from pdfDocument import PdfDocument
from pdfPage import PdfPage
from imagePage import ImagePage

from pic2pdf import image_to_pdf
# import _thread
from pdf_annotate import PdfAnnotator, Location, Appearance



thickness = 1
boxColors = [ (0,0,1), (1, 0, 0), (0,1,0)]    # BRG, x-b-f

"""
# 380 - 450 - 500
 -x -dev kp3 -idpi 500 -odpi 500 -fc- -j 0 -col 1 -bpc 2 -rt 0 -c
 -x -dev kp3 -idpi 450 -odpi 450 -fc- -j 0 -col 1 -bpc 2 -rt 0
 -x -dev kp3 -idpi 380 -odpi 380 -fc- -j 0 -col 1 -bpc 2 -rt 0

300 for 地球物理学报 
"""
# ------------------------
# ScienceDirect
# ------------------------

def main():
    # doc definition
    pdoc = PdfDocument(
        fileName = "2015_Furuya_determination" + '.pdf',
        startPage= 1   ,       # 112
        endPage  = 550,       # 365
        columns  = 2   ,   # 2
        pageDividerPercent = 65 ,   #    65; 35/8
        pageColumnPercents = [48] ,   #    49, [38,69], [26,53,75], [25,38,50,68,76,88]
        k2dpi = 500,
        twoSides=False
        )
    # --------------------------------- 


    if ( os.path.exists(pdoc.logPath) ):
        print("\na log file exists!\n")
        cutOrNot = input("\nWould you like to crop the pdf document?\n(y/n) -- ")
        if (cutOrNot == "y"):
            cropFromLog(pdoc)
        # merge
        # mergeOrNot = input("\nWould you like to merge the cropped pdfs?\n(y/n) -- ")
        mergeOrNot = "y"
        if (mergeOrNot == "y"):
            pdoc.mergeAndReflow()
    # finish
    else:
        # create log file
        f = codecs.open(pdoc.logPath,"w",encoding='utf-8')
        f.close()
    
        # cut using plas
        # cutOrNot = input("\nWould you like to cut the pdf document with plas (page layout analysis)?\n(y/n) -- ")
        cutOrNot = "y"
        if (cutOrNot == "y"):
            print("\nThere is no log file.\nStarting to cut the pdf document with plas (page layout analysis)...\n")
            # 1 convert pdf into images
            pdoc.convert2Image()
            imgPaths = pdoc.originalImagePaths
            
            print("\n")
            with tqdm(total=len(imgPaths), desc="cutting with AI tech...") as pbar:
                for i in range(len(imgPaths)):
                    processPage(i, imgPaths, pdoc)
                    pbar.update(1)
                """
                # for j in range(0, n):
                if (i%n==0):
                    _thread.start_new_thread( processPage, (i, imgPaths, pdoc) )
                    if ( (i + 1) < len(imgPaths) ):
                        _thread.start_new_thread( processPage, (i+1, imgPaths, pdoc) )
                    # print( "page {} on thread {}".format(i+1, j+ 1)   )
                        eval( '_thread.start_new_thread( processPage, (i, imgPaths, pdoc) )' )
                        # processPage(i, imgPaths, pdoc)"""
                """
                # create an object of ImagePage
                imgPage = ImagePage(imgPaths[i], i+1 )

                # crop margins, no functions for paddleocr
                xylu = imgPage.cropMarginsbyPercents()    # x,y,l,u, new origin, point, here are 0,0

                imgPage.layoutAnalysisByPaddle()                                                                                                                            # page layout analysis -  cut! divide!
                imgPage.arrangeLayout(pdoc.columns, pdoc.pageDividerPercent, pdoc.pageColumnPercents)            # arrange layout
                imgPage.saveBlockImage()
                singlePdfPage = PdfPage(pdoc.path, imgPage.path)                                                                                             # back project to pdf page
                # calculate and cut
                infoGroup = [imgPage.textInfoOrdered, imgPage.tableInfoOrdered, imgPage.figureInfoOrdered ]
                labelGroup = ["txt", "tbl", "fig"]
                for (bi, bl) in zip( infoGroup, labelGroup):
                    areaInfo = []
                    for xywh in bi:
                        areas = singlePdfPage.calculatePDFCropArea(xylu,xywh)
                        areaInfo.append( areas )
                    singlePdfPage.cropBlocksByPixel(areaInfo, pdoc.pagepdfFolder, bl)
                    """

            
            pbar.close()
        # pic to pdf for all in original folder
        image_to_pdf(pdoc.path)
    # -------------------------------------------------

# -------------------------------------
def processPage(i, imgPaths, pdoc):
    # image
    # 2 create an object of ImagePage
    pageNo = pdoc.startPage + i - 1
    # pageNo = int( os.path.split(imgPage.path)[-1].strip(".png") )
    imgPage = ImagePage(imgPaths[i], pageNo+1 )

    # 3 crop margins, no functions for paddleocr
    xylu = imgPage.cropMarginsbyPercents()    # x,y,l,u, new origin, point, here are 0,0

    imgPage.layoutAnalysisByPaddle( len(imgPaths)  )    # 4 page layout analysis -  cut! divide!
    imgPage.arrangeLayout(pdoc.columns, pdoc.pageDividerPercent, pdoc.pageColumnPercents)    # 5 arrange layout
    imgPage.saveBlockImage()

    # pdf
    singlePdfPage = PdfPage(pdoc.path, pageNo)    # back project to pdf page
    # calculate and cut
    infoGroup = [imgPage.textInfoOrdered, imgPage.tableInfoOrdered, imgPage.figureInfoOrdered ]
    labelGroup = ["x", "b", "f"]
    for (bi, bl) in zip( infoGroup, labelGroup):
        areaInfo = []
        # write to log file
        f = codecs.open(pdoc.logPath,"a",encoding='utf-8')
        for xywh in bi:
            areas = singlePdfPage.calculatePDFCropArea(xylu,xywh)
            areaInfo.append( areas )
            f.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(pageNo+1, bl, areas[0],areas[1],areas[2],areas[3] ) )
            # page No - label - 
        singlePdfPage.cropBlocksByPixel(areaInfo, pdoc.pagepdfFolder, bl)

        f.close()
# -------------------------
def cropFromLog(doc):

    # delete pdf folder
    print("\nremove the pdf foder and its contents\n")
    shutil.rmtree(doc.fileFolder)
    doc.createFolders()
    
    f = codecs.open(doc.logPath,"r",encoding='utf-8')
    g = f.readlines()
    f.close()
    
    annotator = PdfAnnotator(doc.path)

    startPage = int( (g[0].split())[0]) 
    endPage   = int( (g[-1].split())[0])
    pageAmount = endPage - startPage + 1
    print("{0} pages from log file information\n".format(pageAmount)  )
    with tqdm(total=pageAmount, desc="cropping...") as pbar:
        for i in range(pageAmount):
            singlePdfPage = PdfPage(doc.path, i+startPage)    # back project to pdf page

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
                singlePdfPage.cropBlocksByPixel(areaInfo, doc.pagepdfFolder, bl)

            pbar.update(1)
    pbar.close()

    outpath_annotated = doc.path.replace(".pdf", "_annt.pdf")
    annotator.write(outpath_annotated)


"""
N1-N5 grammar
shoPdf = ShoPDF(
    fileName  = 'testkk.pdf',
    startPage = 229   ,       # 112
    endPage   = 274  ,       # 210
    dilation  = 8,     # 6,4,8
    columns   = 1   ,   # 2
    pageDividerPercent = 65 ,   #    65
    pageColumnPercents = [49] ,   #    0.49, [26,53,75], [25,38,50,68,76,88]
    cutPercents = [     # left, upper is origin
            4,    # 2 left
            6,    # 5 upper    6.8, 7,9 ; 7 for sd new; 
            97,   # 95 right
            89.5],    # 95  bottom    92
    twoSides=False
    )
"""
if __name__ == '__main__':
    start = datetime.datetime.now()
    # --------------
    main()
    # --------------
    end = datetime.datetime.now()
    timeDuration = str(end - start).zfill(4)
    print(end)
    print( 'Time cost -- {}'.format(timeDuration) )


# https://www.geeksforgeeks.org/delete-a-directory-or-file-using-python/