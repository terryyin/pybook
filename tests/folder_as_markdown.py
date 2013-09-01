import unittest
from mock import patch, MagicMock
from py_book import toHTML


class TestConvertFileAndFolder(unittest.TestCase):
    ''' pybook should be able to convert both md File and
        folder into HTML.
    '''
    def setUp(self):
        pass


    def tearDown(self):
        pass


    @patch('py_book.open', create=True)
    def test_convert_MD_file_into_html(self, mock_open):
        mock_open.return_value = MagicMock(spec=file)
        file_handle = mock_open.return_value.__enter__.return_value
        file_handle.read.return_value = "#ABC"
        
        c = toHTML("/path/to/markdown.md")

        mock_open.assert_called_with("/path/to/markdown.md", 'r')
        self.assertEqual("<h1>ABC</h1>", c)
        
