# CV Builder App

A Django-based web application to build professional CVs. Users can input their data, select a layout style, and export the result as a styled PDF.

## ✨ Features

- Input comprehensive CV data:
  - Personal information
  - Summary
  - Education (multiple entries via formset)
  - Work experience with multiple job descriptions (nested formset)
  - Skills and certificates
- 4 Styles CSS (ATR CV Version)
- Export CV to PDF with selected style
- Grid-based layout system for flexible design

## 🛠 Tech Stack

- Python & Django
- HTML + CSS (with CSS Grid for layouting)
- WeasyPrint (for PDF rendering)
- Bootstrap (for basic styling, optional)
- SQLite (default) or MySQL support

## 🚀 Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/username/cv-builder-app.git
   cd cv-builder-app

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
