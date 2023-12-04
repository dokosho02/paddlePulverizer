# PaddlePulverizer

## Introduction

1. page layout analysis of a pdf document
2. text reflow of the pdf document for reading on a kindle paperwhite 3

## Dependencies

Python 3.7.x ~ 3.8.x due to paddle dependency

### Python packages
- pdf processing
  - `PyPDF4`
  - `pdf2image`
  - `pdf-annotate`
- image processing
  - `opencv_contrib_python==4.4.0.46`
  - `opencv-python-headless==4.1.2.30`
  - `Pillow`
- [`Paddle series`](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.2/ppstructure/README_ch.md) - It seems that these packages need to be installed individually.
  - `PaddlePaddle`
  - `Layout-Parser`
  - `PaddleOCR`
- others
  - `tqdm`
  - `loguru`
  - `numpy`
  - `pytesseract`
  - [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot) (optional, <= 13.15)


### Other dependencies
- `poppler` - the dependency of `pdf2image` package
  - [Windows](https://github.com/oschwartz10612/poppler-windows)
  - [Ubuntu](https://stackoverflow.com/questions/32156047/how-to-install-poppler-in-ubuntu-15-04) - `sudo apt-get install -y poppler-utils`
- [`tesseract`](https://github.com/UB-Mannheim/tesseract/) - OCR function for figure caption recognition
  - [Windows](https://github.com/UB-Mannheim/tesseract/wiki/)
  - [Ubuntu](https://techviewleo.com/how-to-install-tesseract-ocr-on-ubuntu/)

### Optional functions

- [`k2pdfopt`](https://www.willus.com/k2pdfopt/) - reflow of pdf text file
  - [Ubuntu](https://www.devmanuals.net/install/ubuntu/ubuntu-20-04-focal-fossa/installing-k2pdfopt-on-ubuntu20-04.html) - `sudo apt-get install k2pdfopt -y`

## Installation

The installation without telegram bot function is as follows:
```sh
py -m pip install -r requirements.txt
py -m pip install paddlepaddle==2.1.1 -i https://mirror.baidu.com/pypi/simple
py -m pip install -U https://paddleocr.bj.bcebos.com/whl/layoutparser-0.0.0-py3-none-any.whl
```
## Usage

### Command line

#### Help

See options in details:
```sh
python pulverizer.py -h
```

#### Page layout analysis
```sh
python pulverizer.py yourfile1.pdf [yourfile2.pdf ...] [-c 1] [-p 1 20]
```

When you run the code for the first time, it will take a while to download model data. After that, page layout analysis will start to work.

Pdf files in the [example](./example) folder show the result.

Then you could edit the `.md` file based on the annotated pdf file (`*_box.pdf` or `*_annotated.pdf`).

line template of the `.md` file

```
1	x	61.87	697.18	104.68	712.64
pageNumber pageType left bottom right top
```

- `pageType`
  - `x` for text
  - `b` for table
  - `f` for figure

#### Crop pdf(s) based on `.md` file and reflow the text
```sh
python pulverizer.py yourfile.pdf [yourfile2.pdf ...] -md [-k 300]
```


The same pattern (arguments) is applied to all `yourfile.pdf`.

### Telegram bot

try [this bot](https://t.me/pulverize_bot) on Telegram (not available not)

But you can set up one by yourself.

#### Settings
##### windows
```cmd
setx PULVERIZER_BOT_TOKEN "your bot token"
```
##### macOS

```sh
export ...
```

##### Linux


#### Functions

##### Basics of Telegram Bot
```sh
/start
```

```sh
/help
```
##### Core

```sh
/pl    # page layout analysis
```

```sh
/pp    # get the .md and box pdf file
```

```sh
/md    # reflow
```


##### file manipulations
```sh
/gp    # get current pdf file name
/sp    # set current pdf file name
```

```sh
/ls    # list current files in your folder
/xk    # send the final reflowed pdf file
/rm    # clear your folder
```

```sh
# send file with file name
/sn yourfilepath  

# rename?
/rn
```

## Problem

It is very difficult to pack the source code together via `pyinstaller` due to the complex structures of `paddle(ocr)` package(s).

## Issues
- [ ] the bottom of rectangle shapes should be lower
- [ ] `pdf-annotate` - rectangle shapes have some drift but the pdf cropping is correct
- [x]  `multiprocess` loses function (change to `concurrent.futures`) - 2023-11-23 - 2023-11-23
- [x] delete the last line of `.md` file - 2022-04-11 - 2022-11-20
- [x] `opencv-python-headless==4.1.2.30` [stackoverflow discussion](https://stackoverflow.com/questions/70537488/cannot-import-name-registermattype-from-cv2-cv2)


## References

- [Sorting list of lists by the first element of each sub-list [duplicate]](https://stackoverflow.com/questions/36955553/sorting-list-of-lists-by-the-first-element-of-each-sub-list)