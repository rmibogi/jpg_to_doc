import unittest
from unittest.mock import patch
from io import StringIO
from main import JpegToDocConverter
import tkinter as tk

class TestJpegToDocConverter(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = JpegToDocConverter(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('tkinter.filedialog.askopenfilename', return_value='path/to/test_image.jpg')
    def test_browse_file(self, mock_askopenfilename):
        self.app.browse_file()
        self.assertEqual(self.app.file_path, 'path/to/test_image.jpg')
        self.assertEqual(self.app.label.cget('text'), 'Выбрано: path/to/test_image.jpg')
        self.assertEqual(self.app.convert_button.cget('state'), tk.NORMAL)

    @patch('tkinter.filedialog.askopenfilename', return_value='')
    def test_browse_file_no_file_selected(self, mock_askopenfilename):
        self.app.browse_file()
        self.assertFalse(hasattr(self.app, 'file_path'))
        self.assertEqual(self.app.label.cget('text'), 'Файл не выбран')
        self.assertEqual(self.app.convert_button.cget('state'), tk.DISABLED)

    @patch('tkinter.filedialog.asksaveasfilename', return_value='path/to/save_result.doc')
    def test_convert_to_doc(self, mock_asksaveasfilename):
        with patch('builtins.open', create=True) as mock_open:
            self.app.file_path = 'path/to/test_image.jpg'
            self.app.convert_to_doc()

            mock_open.assert_called_once_with('path/to/save_result.doc', 'w', encoding='utf-8')
            self.assertTrue(self.app.file_saved)
            self.assertEqual(self.app.label.cget('text'), 'Результат сохранен в path/to/save_result.doc')

    @patch('tkinter.filedialog.asksaveasfilename', return_value='')
    def test_convert_to_doc_no_save_path(self, mock_asksaveasfilename):
        with patch('builtins.open', create=True) as mock_open:
            self.app.file_path = 'path/to/test_image.jpg'
            self.app.convert_to_doc()

            mock_open.assert_not_called()
            self.assertFalse(self.app.file_saved)
            self.assertEqual(self.app.label.cget('text'), 'Файл не выбран')

    def test_preprocess_image(self):
        image_path = 'path/to/test_image.jpg'
        with patch('PIL.Image.open') as mock_open:
            with patch.object(Image.Image, 'convert') as mock_convert:
                with patch.object(Image.Image, 'filter') as mock_filter:
                    self.app.preprocess_image(image_path)

                    mock_open.assert_called_once_with(image_path)
                    mock_convert.assert_called_once_with('L')
                    mock_filter.assert_called_once_with(ImageFilter.GaussianBlur(radius=0.3))

if __name__ == '__main__':
    unittest.main()
