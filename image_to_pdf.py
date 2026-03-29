import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageOps, ImageTk
import os
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ImageToPDFApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Image to PDF Converter")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.eval("tk::PlaceWindow . center")

        self.file_paths = []
        self.thumbnails = []

        self.setup_ui()
        self.root.bind("<Control-o>", lambda _: self.select_images())
        self.root.bind("<Control-Return>", lambda _: self.create_pdf())
        self.root.bind("<Escape>", lambda _: self.clear_images())
    
    def setup_ui(self):
        # Title
        self.title_label = ctk.CTkLabel(self.root, text="Image to PDF Converter", 
                                       font=ctk.CTkFont(size=28, weight="bold"))
        self.title_label.pack(pady=30)
        
        # Browse button (clean, centered)
        self.browse_btn = ctk.CTkButton(self.root, text="📁 Browse Files", 
                                       command=self.select_images, height=50, 
                                       font=ctk.CTkFont(size=20, weight="bold"),
                                       fg_color="#3498db", hover_color="#2980b9")
        self.browse_btn.pack(pady=20)
        
        # Files List
        self.list_frame = ctk.CTkFrame(self.root)
        self.list_frame.pack(pady=10, padx=40, fill="both", expand=True)
        
        self.file_listbox = ctk.CTkScrollableFrame(self.list_frame, label_text="Selected Images (0)", 
                                                  label_font=ctk.CTkFont(size=16, weight="bold"))
        self.file_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Buttons Frame
        self.btn_frame = ctk.CTkFrame(self.root)
        self.btn_frame.pack(pady=20, padx=40, fill="x")
        
        self.clear_btn = ctk.CTkButton(self.btn_frame, text="🗑️ Clear All", 
                                      command=self.clear_images, fg_color="#e74c3c", hover_color="#c0392b")
        self.clear_btn.pack(side="left", padx=15, pady=15)
        
        self.progress = ctk.CTkProgressBar(self.btn_frame, progress_color="#3498db")
        self.progress.pack(side="left", padx=15, pady=15, fill="x", expand=True)
        self.progress.set(0)
        
        self.convert_btn = ctk.CTkButton(self.btn_frame, text="Convert to PDF", 
                                        command=self.create_pdf, height=50, font=ctk.CTkFont(size=18, weight="bold"),
                                        fg_color="#27ae60", hover_color="#2ecc71")
        self.convert_btn.pack(side="right", padx=15, pady=15)
    
    def select_images(self):
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp")]
        )
        self.add_files(files)
    
    def add_files(self, files):
        new_files = 0
        for file_path in files:
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')):
                if file_path not in self.file_paths:
                    self.file_paths.append(file_path)
                    self.create_thumbnail(file_path)
                    new_files += 1
        if new_files > 0:
            self.update_list()
    
    def create_thumbnail(self, file_path):
        try:
            img = Image.open(file_path)
            img = ImageOps.exif_transpose(img).convert('RGB')
            img.thumbnail((100, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.thumbnails.append(photo)
        except Exception:
            self.thumbnails.append(None)
    
    def update_list(self):
        for widget in self.file_listbox.winfo_children():
            widget.destroy()
        
        self.file_listbox.configure(label_text=f"Selected Images ({len(self.file_paths)})")
        
        for i, (path, thumb) in enumerate(zip(self.file_paths, self.thumbnails)):
            frame = ctk.CTkFrame(self.file_listbox, fg_color="transparent")
            frame.pack(fill="x", padx=10, pady=5)
            
            if thumb:
                thumb_label = ctk.CTkLabel(frame, image=thumb, text="", width=100, height=100)
                thumb_label.pack(side="left", padx=(0, 15))
            
            info_frame = ctk.CTkFrame(frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
            
            name_label = ctk.CTkLabel(info_frame, text=os.path.basename(path), 
                                    font=ctk.CTkFont(size=14, weight="bold"), anchor="w")
            name_label.pack(anchor="w")
            
            size_label = ctk.CTkLabel(info_frame, text=f"{os.path.getsize(path) / 1024:.1f} KB", 
                                    text_color="gray70", anchor="w")
            size_label.pack(anchor="w")
            
            remove_btn = ctk.CTkButton(frame, text="❌", width=40, height=40,
                                     command=lambda p=path: self.remove_image(p),
                                     fg_color="#e74c3c", hover_color="#c0392b", font=ctk.CTkFont(size=14))
            remove_btn.pack(side="right")
    
    def remove_image(self, path):
        if path in self.file_paths:
            idx = self.file_paths.index(path)
            self.file_paths.pop(idx)
            self.thumbnails.pop(idx)
            self.update_list()
    
    def clear_images(self):
        self.file_paths.clear()
        self.thumbnails.clear()
        self.update_list()
    
    def create_pdf(self):
        if not self.file_paths:
            messagebox.showwarning("No images", "Please select images first.")
            return

        pdf_path = filedialog.asksaveasfilename(
            title="Save PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        if pdf_path:
            self.progress.set(0)
            self.browse_btn.configure(state="disabled")
            self.clear_btn.configure(state="disabled")
            self.convert_btn.configure(state="disabled", text="🔄 Converting...")
            threading.Thread(target=self._convert_worker, args=(pdf_path,), daemon=True).start()

    def _convert_worker(self, pdf_path):
        try:
            images = []
            for i, f in enumerate(self.file_paths):
                img = ImageOps.exif_transpose(Image.open(f)).convert('RGB')
                images.append(img)
                progress = (i + 1) / len(self.file_paths)
                self.root.after(0, self.progress.set, progress)

            images[0].save(pdf_path, "PDF", resolution=150.0, save_all=True, append_images=images[1:])
            self.root.after(0, lambda: messagebox.showinfo("Success!", f"PDF created successfully!\n\n📄 {pdf_path}"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to create PDF:\n{str(e)}"))
        finally:
            self.root.after(0, self._reset_ui)

    def _reset_ui(self):
        self.progress.set(0)
        self.browse_btn.configure(state="normal")
        self.clear_btn.configure(state="normal")
        self.convert_btn.configure(state="normal", text="Convert to PDF")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ImageToPDFApp()
    app.run()
