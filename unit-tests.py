import unittest
from unittest.mock import patch, Mock
from tkinter import Tk
from main import JpegToDocConverter

class TestJpegToDocConverter(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.converter = JpegToDocConverter(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch("tkinter.filedialog.askopenfilename")
    def test_browse_file_valid_path(self, mock_askopenfilename):
        mock_askopenfilename.return_value = "path/to/image.jpg"
        self.converter.browse_file()
        self.assertEqual(self.converter.file_path, "path/to/image.jpg")
        self.assertEqual(self.converter.label.cget("text"), "Выбрано: path/to/image.jpg")
        self.assertEqual(self.converter.convert_button["state"], "normal")
        self.assertFalse(self.converter.file_saved)

    @patch("tkinter.filedialog.askopenfilename")
    def test_browse_file_invalid_path(self, mock_askopenfilename):
        mock_askopenfilename.return_value = ""
        self.converter.browse_file()
        self.assertNotIn("file_path", dir(self.converter))
        self.assertEqual(self.converter.label.cget("text"), "Файл не выбран")
        self.assertEqual(self.converter.convert_button["state"], "disabled")
        self.assertFalse(self.converter.file_saved)

    @patch("docx.opc.pkgwriter.PhysPkgWriter.write")
    @patch("tkinter.filedialog.asksaveasfilename")
    @patch("PIL.Image.open")
    @patch("pytesseract.image_to_string")
    def test_convert_to_doc(self, mock_image_to_string, mock_image_open, mock_asksaveasfilename,
                            mock_physpkgwriter_write):
        mock_asksaveasfilename.return_value = "path/to/save.doc"
        mock_image_open.return_value = Mock()
        mock_image_to_string.return_value = "Text from image"

        self.converter.browse_file()

        self.converter.convert_to_doc()

        mock_image_open.assert_called_with(self.converter.file_path)
        mock_image_to_string.assert_called_with(mock_image_open.return_value, lang='rus+eng')
        mock_physpkgwriter_write.assert_called_with("path/to/save.doc", self.converter.doc_part.rels,
                                                    self.converter.doc_part.parts)

        self.assertTrue(self.converter.file_saved)
        self.assertIn("Результат сохранен в", self.converter.label.cget("text"))

    @patch("tkinter.filedialog.asksaveasfilename")
    def test_convert_to_doc_cancel_save(self, mock_asksaveasfilename):
        mock_asksaveasfilename.return_value = ""
        self.converter.convert_to_doc()
        self.assertEqual(self.converter.label.cget("text"), "Выберите изображение")
        self.assertFalse(self.converter.file_saved)

if __name__ == "__main__":
    unittest.main()
