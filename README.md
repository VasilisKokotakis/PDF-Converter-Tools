# PDF Converter Tools

A collection of clean, modern desktop apps for converting PDFs and images.
Built with **Python** and **CustomTkinter**, designed to be lightweight, fast, and easy to use.

Currently included:

*  **Image → PDF Converter**
*  **PDF → Word Converter**

Works great on Linux/Debian but runs everywhere Python does.

---

## Tools Included

### Image to PDF Converter

Turn your photos into high-quality PDFs with previews, progress tracking, and perfect orientation.

**File:** `image_to_pdf.py`

#### Features

* **Modern dark UI** with CustomTkinter
* **Image previews** with correct colors
* **File size display** and individual remove buttons
* **Progress bar** during conversion
* **Handles EXIF orientation** automatically
* **High-quality PDF output** (150 DPI)
* **Super lightweight** – no bloat

---

### PDF to Word Converter

Extract text from PDF files and save it as a Word document.

**File:** `pdf_to_word.py`

#### Features

* **Modern dark UI** with CustomTkinter
* **PDF file selection**
* **Page-by-page text extraction**
* **Progress bar** during conversion
* **Exports to `.docx` format**

**Note:**
This tool extracts **text only**. Images, tables, and complex formatting are not preserved.

---

## Quick Start

### Clone & install

```bash
git clone https://github.com/VasilisKokotakis/PDF-Converter-Tools.git
cd PDF-Converter
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

### Run a tool

**Image → PDF**

```bash
python image_to_pdf.py
```

**PDF → Word**

```bash
python pdf_to_word.py
```

---

### Use it

* Select your files
* Preview / confirm
* Click **Convert**
* Save your output

All processing is **100% local**.

---

## Tech Stack

* **Python 3.12+**
* [CustomTkinter](https://customtkinter.tomschimansky.com/) – Modern UI
* [Pillow](https://pillow.readthedocs.io/) – Image processing
* [pdfplumber](https://github.com/jsvine/pdfplumber) – PDF text extraction
* [python-docx](https://python-docx.readthedocs.io/) – Word document generation

---

## requirements.txt

```txt
customtkinter
pillow
pdfplumber
python-docx
```

---

## Pro Tips

* **Phone photos?** EXIF rotation handled automatically
* **Large batches?** Progress bars show real-time status
* **Works offline** – no uploads, no tracking
* **Executable builds:** PyInstaller supported

---

## Contributing

Found a bug or have an idea? PRs are welcome!

```
1. Fork the repo
2. Create your feature branch (git checkout -b my-cool-feature)
3. Commit changes (git commit -m "Add cool feature")
4. Push (git push origin my-cool-feature)
5. Open a Pull Request
```

