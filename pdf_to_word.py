import customtkinter as ctk
from tkinter import filedialog, messagebox
from docx import Document
import pdfplumber
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class PDFtoWordApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("PDF to Word Converter")
        self.root.geometry("700x400")
        self.root.resizable(False, False)
        self.root.eval("tk::PlaceWindow . center")

        self.pdf_path = None

        self.setup_ui()

    def setup_ui(self):
        # Title
        title = ctk.CTkLabel(
            self.root,
            text="PDF to Word Converter",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=30)

        # Selected file label
        self.file_label = ctk.CTkLabel(
            self.root,
            text="No PDF selected",
            font=ctk.CTkFont(size=14),
            text_color="gray80",
            wraplength=600
        )
        self.file_label.pack(pady=10)

        # Buttons frame
        btn_frame = ctk.CTkFrame(self.root)
        btn_frame.pack(pady=30)

        self.select_btn = ctk.CTkButton(
            btn_frame,
            text="📄 Select PDF",
            command=self.select_pdf,
            width=160,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.select_btn.grid(row=0, column=0, padx=10)

        self.convert_btn = ctk.CTkButton(
            btn_frame,
            text="Convert to Word",
            command=self.convert_to_word,
            width=200,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#27ae60",
            hover_color="#2ecc71"
        )
        self.convert_btn.grid(row=0, column=1, padx=10)

        # Progress
        self.progress = ctk.CTkProgressBar(
            self.root,
            progress_color="#3498db",
            width=500
        )
        self.progress.pack(pady=10)
        self.progress.set(0)

    def select_pdf(self):
        path = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf")]
        )
        if path:
            self.pdf_path = path
            self.file_label.configure(
                text=f"Selected: {os.path.basename(path)}"
            )

    def convert_to_word(self):
        if not self.pdf_path:
            messagebox.showwarning("No file", "Please select a PDF first.")
            return

        save_path = filedialog.asksaveasfilename(
            title="Save Word file as",
            defaultextension=".docx",
            filetypes=[("Word Document", "*.docx")]
        )
        if not save_path:
            return

        try:
            self.progress.set(0)
            self.convert_btn.configure(state="disabled", text="Converting...")
            self.root.update()

            doc = Document()
            with pdfplumber.open(self.pdf_path) as pdf:
                total_pages = len(pdf.pages)
                for i, page in enumerate(pdf.pages, start=1):
                    text = page.extract_text() or ""
                    if text.strip():
                        for line in text.split("\n"):
                            doc.add_paragraph(line)
                    if i < total_pages:
                        doc.add_page_break()

                    self.progress.set(i / total_pages)
                    self.root.update()

            doc.save(save_path)

            messagebox.showinfo(
                "Success",
                f"Word document created:\n{save_path}"
            )
        except Exception as e:
            if "password" in str(e).lower() or "encrypted" in str(e).lower():
                messagebox.showerror("Protected PDF", "This PDF is password-protected and cannot be converted.")
            else:
                messagebox.showerror("Error", f"Conversion failed:\n{e}")
        finally:
            self.progress.set(0)
            self.convert_btn.configure(state="normal", text="Convert to Word")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = PDFtoWordApp()
    app.run()
