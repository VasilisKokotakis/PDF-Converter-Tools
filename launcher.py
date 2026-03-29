import customtkinter as ctk
import subprocess
import sys
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

HERE = os.path.dirname(os.path.abspath(__file__))


class LauncherApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("PDF Converter Tools")
        self.root.geometry("400x280")
        self.root.resizable(False, False)
        self.root.eval("tk::PlaceWindow . center")

        self.setup_ui()

    def setup_ui(self):
        ctk.CTkLabel(
            self.root,
            text="PDF Converter Tools",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(35, 5))

        ctk.CTkLabel(
            self.root,
            text="Choose a tool to open",
            font=ctk.CTkFont(size=14),
            text_color="gray70"
        ).pack(pady=(0, 30))

        ctk.CTkButton(
            self.root,
            text="Image → PDF",
            command=lambda: self._launch("image_to_pdf.py"),
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(padx=50, pady=8, fill="x")

        ctk.CTkButton(
            self.root,
            text="PDF → Word",
            command=lambda: self._launch("pdf_to_word.py"),
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#27ae60",
            hover_color="#2ecc71"
        ).pack(padx=50, pady=8, fill="x")

    def _launch(self, script):
        subprocess.Popen([sys.executable, os.path.join(HERE, script)])

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    LauncherApp().run()
