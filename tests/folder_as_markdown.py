''' Tests For Converting File or Folder into HTML
'''
import unittest
from mock import patch, MagicMock, call
import os
from py_book import to_html


@patch("os.path.isfile", create=True)
@patch.object(os, 'listdir')
@patch('codecs.open', create=True)
class TestConvertFileAndFolder(unittest.TestCase):
    ''' pybook should be able to convert both md File and
        folder into HTML.
    '''
    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_convert_md_file(self, mock_open, _, mock_isfile):
        mock_isfile.return_value = True
        mock_open.return_value = MagicMock()
        file_handle = mock_open.return_value.__enter__.return_value
        file_handle.read.return_value = "#ABC"

        html = to_html("/path/to/markdown.md")

        mock_open.assert_called_with("/path/to/markdown.md", 'r', encoding='utf-8')
        self.assertEqual("<h1>ABC</h1>", html)


    def test_convert_folder(self, mock_open, mock_listdir, mock_isfile):
        mock_isfile.side_effect = [False, True]
        mock_listdir.return_value = ['a.md']
        mock_open.return_value = MagicMock()
        file_handle = mock_open.return_value.__enter__.return_value
        file_handle.read.return_value = "#ABC"

        html = to_html("/path/to/folder")

        mock_open.assert_called_with("/path/to/folder/a.md", 'r', encoding='utf-8')
        self.assertEqual("<h1>ABC</h1>", html)


    def test_convert_folder_with_no_init_file(self, mock_open, mock_listdir, mock_isfile):
        ''' Should combine files in alphabetical order.
        '''
        mock_isfile.side_effect = [False, True, True]
        mock_listdir.return_value = ['b.md', 'a.md']
        mock_open.return_value = MagicMock()
        file_handle = mock_open.return_value.__enter__.return_value
        file_handle.read.side_effect = ["#A", "#B"]

        html = to_html("/path/to/folder")

        self.assertEqual(mock_open.call_args_list, 
                         [call("/path/to/folder/a.md", "r", encoding='utf-8'), 
                          call("/path/to/folder/b.md", "r", encoding='utf-8')])
        self.assertEqual("<h1>A</h1>\n<h1>B</h1>", html)
