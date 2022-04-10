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
- [`Paddle series`](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.2/ppstructure/README_ch.md)
  - `PaddlePaddle`
  - `Layout-Parser`
  - `PaddleOCR`
- others
  - `tqdm`
  - `loguru`
  - `pytesseract`

- Telegram bot
  - [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
  - [`magic`](https://github.com/ahupp/python-magic) - file type identification
    - `pip install python-magic-bin==0.4.14` - [GitHub discussion](https://github.com/Yelp/elastalert/issues/1927/)
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

```cmd
setx PULVERIZER_BOT_TOKEN "your bot token"
```


```sh
/start
```

```sh
/help
```

```sh
/pl
```

```sh
/rn
```


```sh
/md
```


```sh
/ls
/xk
/rm
/sn
```

## Problem

It is very difficult to pack the source code together via `pyinstaller` due to the complex structures of `paddle(ocr)` package(s).

## Issues

- `opencv-python-headless==4.1.2.30` [stackoverflow discussion](https://stackoverflow.com/questions/70537488/cannot-import-name-registermattype-from-cv2-cv2)