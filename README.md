## IGNOU date-sheet extractor
 Extract the date-sheet from pdf provided by IGNOU in a json file.
### Requirements
 It requires [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/installation/) installed and working. Tested with version 1.14.8.

### Steps
 * For final date-sheet, run `python ftee_date_sheet.py filename.pdf output_filename`.
 * For tentative date-sheet, run `python ttee_date_sheet.py filename.pdf output_filename`.