#!/usr/local/bin/python3
import argparse
from datetime import datetime
from cut_merge_k2 import cutAndMerge

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


appHeader = f"{bcolors.HEADER}Page layout analysis for pdf document{bcolors.ENDC}"

# ----------------------
def main():
    # Initialize parser
    parser = argparse.ArgumentParser(description=appHeader,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Adding positional Argument
    parser.add_argument("pdfs",
        type=str,
        nargs='+',    # 1 or more arguments
        help = "PDF file name/path")

    # Adding optional argument
    parser.add_argument("-c","--column", 
        type=int,
        default=2,
        help = "column(s) of the pdf document")

    parser.add_argument("-p", "--pagerange",
        type=int,
        default=[1,500],
        nargs=2,    # two arguments
        help = "page range to process")

    parser.add_argument("-k", "--kdpi",
        type=int,
        default=500,
        help = "dpi value for k2pdfopt reflow text")

    parser.add_argument("-md","--markdown", 
        action='store_true',
	    default=False,
        help = "re-crop pdf based on .md file")

    # Read arguments from command line
    args = parser.parse_args()
    
    print(appHeader)
    print(f"{bcolors.OKCYAN}These files will be processed:")
    [print(f"\t{pdf}") for pdf in args.pdfs]
    print(f"{bcolors.ENDC}")

    print(args.pagerange)

    for pdf in args.pdfs:
        cutAndMerge(
            pdfName=pdf,
            startPage=args.pagerange[0],
            endPage  =args.pagerange[1],
            col=args.column,
            k2dpi=args.kdpi,
            mdtf = args.markdown,
        )

if __name__ == '__main__':
    start = datetime.now()
    print(start)
    # --------------
    main()
    # --------------
    end = datetime.now()
    timeDuration = str(end - start).zfill(4)
    print(end)
    print( 'Time cost -- {}'.format(timeDuration) )

