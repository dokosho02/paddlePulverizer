from PIL import Image
import cv2
import numpy as np

from loguru import logger
from tqdm import tqdm

from arrangement import arrangeOrder

import pytesseract

# from block import Block

deleteLimit=28
padding = 10

# Blue color in BGR
boxColors = [(255, 0, 0), (0,255,0), (0,0,255)]
# Line thickness of 2 px
thickness = 2

# font
font = cv2.FONT_HERSHEY_TRIPLEX

# fontScale
fontScale = 4

textColors = [ [0, 125, 255], [125,0,255], [0,255, 125] ]

def saveImage(imgPg, pathName, blockInfo, blockLabel, box_color, text_color):
        count = 1
        for c in blockInfo:
            x,y,w,h = c
            xl = x #- padding
            yl = y
            xr = x+w #+ padding
            yr = y+h
            imageBlock = imgPg[ yl: yr, xl: xr]

            output_path =pathName.replace('.png', '_'+ blockLabel +  '_' + str(count*2).zfill(2) +'.png').replace("original","cut" )
            cv2.imwrite(output_path, imageBlock)

            # draw boxes around block
            start_point = (xl, yl)  # represents the top left corner of rectangle
            end_point = (xr, yr)  # represents the bottom right corner of rectangle
            org = ( (xl , int( (yl + yr)/2 )) )

            # color = colors[0]
            # if (blockLabel=="b"):
            #     color = colors[1]
            # elif (blockLabel=="f"):
            #     color = colors[2]

            img_plotted = cv2.rectangle(imgPg, start_point, end_point, box_color, thickness)
   
            # Using cv2.putText() method
            img_plotted = cv2.putText(img_plotted, str(count), org, font, fontScale, text_color, thickness, cv2.LINE_AA)

            cv2.imwrite(pathName, img_plotted)

            count += 1

# --------------------------------------------------
class ImagePage():
    def __init__(self, imagePath, pageNo):
        self.path = imagePath         # String
        self.onPageNo = pageNo    # Int

        # self.blocks   = []
        self.figureBlockUnordered = []
        self.textBlockUnordered  = []
        self.tableBlockUnordered = []
        self.captionBlockUnordered = []
        
        self.titleBlockUnordered = []
        self.equationBlockUnordered = []

    # ---------------------------------------
    def cropMarginsbyPercents(self):
        img = Image.open(self.path)
        x, y = img.size
        l,u = ( 0, 0 )
        return [x,y,l,u]
    # ------------------------------------------------------
    def layoutAnalysisByPaddle(self, totalPageNumber):
        from paddleocr import PPStructure

        table_engine = PPStructure( show_log=False,use_gpu=False )
        img = cv2.imread(self.path)
        self.pagewidth = img.shape[1]

        result = table_engine(img)

        for rs in result:
            box = rs["bbox"]
            blockType = rs["type"]
            print( (self.onPageNo, totalPageNumber, blockType, box) )

            # convert to xywh
            xl,yl,xr,yr = box
            x,y,w,h = xl -padding ,yl, xr + padding*2 -xl, yr-yl

            if (blockType=="Table"):
                self.tableBlockUnordered.append( [x,y,w,h] )
            elif (blockType=="Figure"):
                self.figureBlockUnordered.append( [x,y,w,h] )
            else:
                subImg = img[ y: y+h, x: x+w]
                ocredTxt = pytesseract.image_to_string(subImg, lang="eng")
                if ( ocredTxt.startswith("Fig") or  ocredTxt.startswith("FIG")  ):
                    self.figureBlockUnordered.append( [x,y,w,h] )
                elif ( ocredTxt.startswith("Tab") or ocredTxt.startswith("TAB") ):
                    self.tableBlockUnordered.append( [x,y,w,h] )
                else:
                    self.textBlockUnordered.append( [x,y,w,h] )

            # newBlock = Block( xywh=[x,y,w,h], grouped=rs["type"] )
    # ------------------------------------------------------
    def arrangeLayout(self,columns,pageDividerPercent,pageColumnPercents):
        self.textInfoOrdered   = arrangeOrder(self.textBlockUnordered,   self.pagewidth, columns, pageDividerPercent, pageColumnPercents)
        self.tableInfoOrdered  = arrangeOrder(self.tableBlockUnordered,  self.pagewidth, columns, pageDividerPercent, pageColumnPercents)
        self.figureInfoOrdered = arrangeOrder(self.figureBlockUnordered, self.pagewidth, columns, pageDividerPercent, pageColumnPercents)
    # ---------------------------------------
    def saveBlockImage(self):
        # loading images
        imgPg = cv2.imread(self.path)

        infoGroup = [self.textInfoOrdered, self.tableInfoOrdered, self.figureInfoOrdered ]
        labelGroup = ["x", "b", "f"]
        for (bi, bl, bc, tc) in zip( infoGroup, labelGroup, boxColors, textColors):
            saveImage(imgPg, self.path, bi, bl, bc, tc)
        """
        count = 1
        for c in self.textInfoOrdered:
            x,y,w,h = c
            imageBlock = image1[y-1:y+h, x-1:x+w]

            output_path = "txt_" + self.path.replace('.png', '_' + str(count*2).zfill(2) +'.png').replace("original","cut" )
            cv2.imwrite(output_path, imageBlock)
            count += 1
            """

