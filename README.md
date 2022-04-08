
# PaddlePulverizer

page layout analysis of pdf document


## Usage
run following command to see help
```sh
python3 pulverizer.py -h
```

## denpendencies

### Python packages
- `PyPDF4`
- `pdf-annotate`
- `pdf2image`
- [`Paddle series`](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.2/ppstructure/README_ch.md)
  - `PaddlePaddle`
  - `Layout-Parser`
  - `PaddleOCR`
### Other dependencies

- `poppler` - the dependency of `pdf2image` package
  - [for windows](https://blog.alivate.com.au/poppler-windows/)
- [`tesseract`](https://github.com/UB-Mannheim/tesseract/) - OCR function for figure caption recognition
  - [for windows](https://github.com/UB-Mannheim/tesseract/wiki/)


### optional functions

- [`k2pdfopt`](https://www.willus.com/k2pdfopt/) - reflow of pdf text file

