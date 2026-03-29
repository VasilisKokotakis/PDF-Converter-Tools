# PDF Converter Tools

A collection of clean, modern desktop apps for converting PDFs and images.
Built with **Python** and **CustomTkinter**, designed to be lightweight, fast, and easy to use.

- **Image → PDF Converter**
- **PDF → Word Converter**
- **Launcher** – open either tool from one place

Works great on Linux/Debian but runs everywhere Python does.

---

## Tools Included

### Launcher

A simple entry point to open either tool without using the terminal.

**File:** `launcher.py`

---

### Image → PDF Converter

Turn your photos into high-quality PDFs with previews, progress tracking, and perfect orientation.

**File:** `image_to_pdf.py`

#### Features

- **Modern dark UI** with CustomTkinter
- **Drag-and-drop** image files directly onto the list
- **Image previews** with correct colors
- **File size display** and individual remove buttons
- **Reorder images** with up/down buttons before converting
- **Non-blocking conversion** – UI stays responsive during export
- **Progress bar** during conversion
- **Handles EXIF orientation** automatically
- **High-quality PDF output** (150 DPI)
- **Keyboard shortcuts:** `Ctrl+O` open, `Ctrl+Enter` convert, `Escape` clear

---

### PDF → Word Converter

Extract text from PDF files and save as a Word document.

**File:** `pdf_to_word.py`

#### Features

- **Modern dark UI** with CustomTkinter
- **File info display** – shows file size and page count after selecting
- **Non-blocking conversion** – UI stays responsive during export
- **Progress bar** during conversion
- **Exports to `.docx` format**
- **Friendly error** for password-protected PDFs
- **Keyboard shortcuts:** `Ctrl+O` open, `Ctrl+Enter` convert, `Escape` clear

**Note:**
This tool extracts **text only**. Images, tables, and complex formatting are not preserved.

---

## Quick Start

### Option A – Pre-built binary (no Python needed)

Download the latest release from the [Releases](https://github.com/VasilisKokotakis/PDF-Converter-Tools/releases) page and run:

```bash
chmod +x PDFConverterTools
./PDFConverterTools
```

### Option B – Run from source

```bash
git clone https://github.com/VasilisKokotakis/PDF-Converter-Tools.git
cd PDF-Converter-Tools
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

#### Run the launcher

```bash
python launcher.py
```

#### Or run a tool directly

```bash
python image_to_pdf.py
python pdf_to_word.py
```

---

## Tech Stack

- **Python 3.12+**
- [CustomTkinter](https://customtkinter.tomschimansky.com/) – Modern UI
- [Pillow](https://pillow.readthedocs.io/) – Image processing
- [tkinterdnd2](https://github.com/Eliav2/tkinterdnd2) – Drag-and-drop support
- [pdfplumber](https://github.com/jsvine/pdfplumber) – PDF text extraction
- [python-docx](https://python-docx.readthedocs.io/) – Word document generation

---

## Tests

```bash
python -m pytest tests/ -v
```

22 tests covering list logic, conversion output, and error handling.

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
