import tkinter as tk
from tkinter import filedialog
from PIL import Image
import pytesseract
from docx import Document

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class JpegToDocConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Doc Converter")
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Выберите изображение:")
        self.label.pack(pady=10)

        self.browse_button = tk.Button(self.root, text="Выбрать", command=self.browse_image)
        self.browse_button.pack(pady=10)

        self.convert_button = tk.Button(self.root, text="Преобразовать", command=self.convert_image_to_doc)
        self.convert_button.pack(pady=10)

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        self.image_path = file_path
        self.label.config(text=f"Выбрано изображение: {file_path}")

    def convert_image_to_doc(self):
        if hasattr(self, 'image_path'):
            image = Image.open(self.image_path)
            text = pytesseract.image_to_string(image, lang='rus')

            doc = Document()
            doc.add_paragraph(text)

            save_path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word files", "*.docx")])
            doc.save(save_path)
            self.label.config(text=f"Результат сохранен в {save_path}")
        else:
            self.label.config(text="Сначала выберите изображение!")


root = tk.Tk()
root.geometry('700x200+200+100')
app = JpegToDocConverter(root)
root.mainloop()
