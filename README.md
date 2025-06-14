# CV Builder App

A Django-based web application to build professional CVs. Users can input their data, select a layout style, and export the result as a styled PDF.

## ✨ Features

  - Input comprehensive CV data:
  - Personal information
  - Summary
  - Education (multiple entries via formset)
  - Work experience with multiple job descriptions (nested formset)
  - Skills and certificates
  - 2 Styles CSS (ATR CV Version) so far
  - Export CV to PDF with selected style 

## 🛠 Tech Stack

- Python & Django
- HTML + CSS (with CSS Grid for layouting)
- WeasyPrint (for PDF rendering)
- Bootstrap (for basic styling, optional)
- MySQL support

 ## Chalengge
 - Can't use CSS grid and Flexbox because the share hosting only support library weasyprint that not support for Grid

