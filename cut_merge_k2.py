# from tqdm import tqdm
# import datetime, os, codecs

# customize
# from pdfDocument import PdfDocument

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
col_div_percents = [
    [1, 0, [0] ],
    [2, 65, [48] ],
    [3, 35, [38,69] ],
]


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


# https://www.geeksforgeeks.org/delete-a-directory-or-file-using-python/