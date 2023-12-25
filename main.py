import sys
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from docx import Document

current_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
tesseract_path = os.path.join(current_dir, 'tesseract-ocr/tesseract.exe')
pytesseract.pytesseract.tesseract_cmd = tesseract_path

class JpegToDocConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Преобразование текста из формата jpg в формат doc")
        self.create_widgets()

    def create_widgets(self):
        font = ('Arial', 14)

        self.label = tk.Label(self.root, text="Выберите изображение", font=font, wraplength=600)
        self.label.pack(pady=10)

        self.browse_button = tk.Button(self.root, text="Выбрать", command=self.browse_file, font=font)
        self.browse_button.pack(pady=10)

        self.convert_button = tk.Button(self.root, text="Преобразовать", command=self.convert_to_doc, font=font)
        self.convert_button.pack(pady=10)
        self.convert_button.config(state=tk.DISABLED)

        self.file_saved = False

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.file_path = file_path
            self.label.config(text=f"Выбрано: {file_path}")
            self.convert_button.config(state=tk.NORMAL)
            self.file_saved = False
        else:
            self.label.config(text="Файл не выбран")
            self.convert_button.config(state=tk.DISABLED)

    def convert_to_doc(self):
        if hasattr(self, 'file_path'):
            preprocessed_image = self.preprocess_image(self.file_path)
            text = pytesseract.image_to_string(preprocessed_image, lang='rus+eng')

            doc = Document()
            doc.add_paragraph(text)

            save_path = filedialog.asksaveasfilename(defaultextension=".doc", filetypes=[("Word files", "*.doc")])
            if save_path:
                doc.save(save_path)
                self.label.config(text=f"Результат сохранен в {save_path}")
                self.file_saved = True

    def preprocess_image(self, image_path):
        image = Image.open(image_path)
        image = image.convert("L")
        image = image.filter(ImageFilter.GaussianBlur(radius=0.3))
        return image

root = tk.Tk()
root.geometry('700x250+200+100')
root.resizable(False, False)
app = JpegToDocConverter(root)
root.mainloop()
