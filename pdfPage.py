from PyPDF4 import PdfFileWriter, PdfFileReader, PdfFileMerger
import os
import shutil
from loguru import logger
from tqdm import tqdm


digital_number = 3    # for image and pdf, digital number

# a page is also an Object
# 

class PdfPage():
    def __init__(self, PDFdocpath, pageNo, verticalWriting=False, right2left=False):
        self.PDFpath    = PDFdocpath
        self.pageNumber = pageNo
        # self.pdfCropArea = []

        in_f = open(self.PDFpath, "rb")
        input1 = PdfFileReader(in_f)
        singlePage = input1.getPage(self.pageNumber-1)   # get pdf page by pagenumber
        
        # pdf page size
        self.pdfPagewidth  = int( singlePage.mediaBox.getUpperRight_x() )
        self.pdfPageheight = int( singlePage.mediaBox.getUpperRight_y() )
        in_f.close()

    def rotate(self):
        # treat vertical direction such as Japanese text page
        pass
    # -------------------------------------
    def calculatePDFCropArea(self, xylu, xywh):

        lon,lat,l,u = xylu    # image, in cropped 
        x,y, w,h    = xywh    # image, in cropped 
        
        # back to the position in original image
        xInOriginal = float(l+x)
        yInOriginal = float(u+y)

        # w,h in PDF
        wPDF = self.pdfPagewidth *(w*1.0/lon)
        hPDF = self.pdfPageheight*(h*1.0/lat)

        xInPDF =  self.pdfPagewidth*(xInOriginal*1.0/lon)
        yInPDF =  self.pdfPageheight*( 1 - (yInOriginal+ h)*1.0/lat)

        xEndPDF = xInPDF + wPDF
        yEndPDf = yInPDF + hPDF

        area = [round(xInPDF,2), round(yInPDF,2), round(xEndPDF,2), round(yEndPDf,2) ]
        return area
    # -------------------------------------
    def cropBlocksByPixel(self, areaInfo, pagepdfFolder, pdfBlockLabel):

        def pageBlockCrop(page, area):
            l,b,r,u= area
            # crop pdf page
            page.trimBox.lowerLeft = (l, b)
            page.trimBox.upperRight =(r, u)

            # left, bottom is the origin
            page.cropBox.lowerLeft = (l, b)
            page.cropBox.upperRight =(r, u)
            return page

        for t in range( len(areaInfo) ):
            output = PdfFileWriter()
            # define the output path
            x = str(self.pageNumber).zfill(digital_number)
            y = str( (t+1)*2 ).zfill(2)
            pulverizedPdfName = '{0}_{1}_{2}.pdf'.format(x, pdfBlockLabel, y)

            pdf_out_path = os.path.join( pagepdfFolder, pulverizedPdfName )
            if (pdfBlockLabel=="f") or (pdfBlockLabel=="b") :
                pdf_out_path = os.path.join( pagepdfFolder, pdfBlockLabel , pulverizedPdfName )

            # cut pdf page
            in_f = open(self.PDFpath, "rb")
            input1 = PdfFileReader(in_f)
            page = input1.getPage(self.pageNumber-1)
            block = pageBlockCrop( page, areaInfo[t] )
            output.addPage(block)
            out_f = open(pdf_out_path, "wb")
            output.write(out_f)
        
            out_f.close()
            in_f.close()
