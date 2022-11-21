# PaddlePulverizer

## Introduction

page layout analysis of pdf document

and then reflow the pdf document for reading on kindle paperwhite 3 using [`k2pdfopt`](https://www.willus.com/k2pdfopt/)



## Denpendencies

### Python packages
- pdf processing
  - `PyPDF4`
  - `pdf-annotate`
  - `pdf2image`
- image processing
  - `opencv_contrib_python>=4.4.0.46`
  - `opencv-python-headless==4.1.2.30`
  - `Pillow`
- [`Paddle series`](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.2/ppstructure/README_ch.md) - It seems that these packages need to be installed individually.
  - `PaddlePaddle`
  - `Layout-Parser`
  - `PaddleOCR`
- others
  - `tqdm`
  - `loguru`
  - `pytesseract`

- Telegram bot
  - [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
### Other dependencies
- `poppler` - the dependency of `pdf2image` package
  - [for windows](https://blog.alivate.com.au/poppler-windows/)
- [`tesseract`](https://github.com/UB-Mannheim/tesseract/) - OCR function for figure caption recognition
  - [for windows](https://github.com/UB-Mannheim/tesseract/wiki/)

### Optional functions

- [`k2pdfopt`](https://www.willus.com/k2pdfopt/) - reflow of pdf text file


## Usage

### Command line

#### Help
```sh
python pulverizer.py -h
```

#### Page layout analysis
```sh
python pulverizer.py yourfile1.pdf [yourfile2.pdf ...] [-c 1] [-p 1 20]
```
then you could edit the `.md` file

#### Crop pdf(s) based on `.md` file and reflow the text
```sh
python pulverizer.py yourfile.pdf [yourfile2.pdf ...] -md [-k 300]
```


The same pattern (arguments) is applied to all `yourfile.pdf`.

### Telegram bot

try [this bot](https://t.me/pulverize_bot) on Telegram

#### Settings
##### windows
```cmd
setx PULVERIZER_BOT_TOKEN "your bot token"
```
##### macOS

##### Linux


#### Functions

#### Basics of Telegram Bot
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
- [x] delete the last line of `.md` file - 2022-04-11 - 2022-11-20

- [x] `opencv-python-headless==4.1.2.30` [stackoverflow discussion](https://stackoverflow.com/questions/70537488/cannot-import-name-registermattype-from-cv2-cv2)


## References

- [Sorting list of lists by the first element of each sub-list [duplicate]](https://stackoverflow.com/questions/36955553/sorting-list-of-lists-by-the-first-element-of-each-sub-list)