'''__init__.md in a folder should contain the definition of the structure of the book.
'''
import unittest

from py_book import from_source_tree_to_markdown
from py_book.markdown_extensions import embed_value


class TestDefintions(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_meta_data(self):
        sources = ["Name: Value\nName2:Value2\n"]
        html = from_source_tree_to_markdown(sources)
        self.assertNotIn("Name", html)
        self.assertNotIn("Value", html)
        

    def test_define_chapter_prefix(self):
        sources = ["chapter_prefix: Chapter " + embed_value("chapter_count") + "\n" +
                   "# Title"]
        html = from_source_tree_to_markdown(sources)
        self.assertIn("Chapter 1 Title", html)
        

    def test_define_chapter_prefix_with_more_chapters(self):
        sources = ["chapter_prefix: Chapter " + embed_value("chapter_count") + "\n" +
                   "# Title1\n"+
                   "# Title2"]
        html = from_source_tree_to_markdown(sources)
        self.assertIn("Chapter 2 Title2", html)
        

    def test_count_appendix(self):
        sources = ["chapter_count: A \n" +
                   "chapter_prefix: Appendix " + embed_value("chapter_count") + "\n" +
                   "# Title1\n"+
                   "# Title2"]
        html = from_source_tree_to_markdown(sources)
        self.assertIn("Appendix B Title2", html)


    def test_mulitple_files_in_the_same_folder(self):
        sources = ["chapter_prefix: Chapter " + embed_value("chapter_count") + "\n# Title1\n",
                   "# Title2"]
        html = from_source_tree_to_markdown(sources)
        self.assertIn("Chapter 2 Title2", html)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()