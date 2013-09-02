'''__init__.md in a folder should contain the definition of the structure of the book.
'''
import unittest

from py_book import from_source_tree_to_markdown
from py_book.markdown_extensions import embed_value


class TestDefault(unittest.TestCase):
    
    def test_(self):
        sources = ["# Title1\n"+
                   "## Section1"]
        html = from_source_tree_to_markdown(sources)
        self.assertEqual("<h1>Title1</h1>\n<h2>Section1</h2>", html)


class TestAutoChapter(unittest.TestCase):

    def test_meta_data(self):
        sources = ["Name: Value\nName2:Value2\n"]
        html = from_source_tree_to_markdown(sources)
        self.assertNotIn("Name", html)
        self.assertNotIn("Value", html)
        

    def test_define_chapter_prefix(self):
        sources = ["chapter_prefix: Chapter " + embed_value("chapter_id") + "\n" +
                   "# Title"]
        html = from_source_tree_to_markdown(sources)
        self.assertIn("Chapter 1 Title", html)
        

    def test_define_chapter_prefix_with_more_chapters(self):
        sources = ["chapter_prefix: Chapter " + embed_value("chapter_id") + "\n" +
                   "# Title1\n"+
                   "# Title2"]
        html = from_source_tree_to_markdown(sources)
        self.assertIn("Chapter 2 Title2", html)
        

    def test_count_appendix(self):
        sources = ["next_chapter_id: A \n" +
                   "chapter_prefix: Appendix " + embed_value("chapter_id") + "\n" +
                   "# Title1\n"+
                   "# Title2"]
        html = from_source_tree_to_markdown(sources)
        self.assertIn("Appendix B Title2", html)


    def test_mulitple_files_in_the_same_folder(self):
        sources = ["chapter_prefix: Chapter " + embed_value("chapter_id") + "\n# Title1\n",
                   "# Title2"]
        html = from_source_tree_to_markdown(sources)
        self.assertIn("Chapter 2 Title2", html)


class TestAutonSections(unittest.TestCase):
    
    def test_section_meta(self):
        sources = ["section_level: 2\n" +
                   "# Title1\n"+
                   "## Section1.1"]
        html = from_source_tree_to_markdown(sources)
        self.assertIn("1.1 Section1.1", html)

    
    def test_section_id_has_chapter_id(self):
        sources = ["section_level: 2\n" +
                   "# Title1\n"+
                   "# Title2\n"+
                   "## Section2.1"]
        html = from_source_tree_to_markdown(sources)
        self.assertIn("2.1 Section2.1", html)

    
    def test_section_id_has_section_id(self):
        sources = ["section_level: 2\n" +
                   "# Title1\n"+
                   "## Section1.1\n"+
                   "## Section1.2"]
        html = from_source_tree_to_markdown(sources)
        self.assertIn("1.2 Section1.2", html)

    
    def test_section_id_restart_in_new_chapter(self):
        sources = ["section_level: 2\n" +
                   "# Title1\n"+
                   "## Section1.1\n"+
                   "# Title2\n"+
                   "## Section2.1"]
        html = from_source_tree_to_markdown(sources)
        self.assertIn("2.1 Section2.1", html)

    
    def test_more_levels(self):
        sources = ["section_level: 3\n" +
                   "# Title1\n"+
                   "## Section1.1\n"+
                   "### Section1.1.1"]
        html = from_source_tree_to_markdown(sources)
        self.assertIn("1.1.1 Section1.1.1", html)

    
    def test_extra_level_should_not_have_prefix(self):
        sources = ["section_level: 2\n" +
                   "# Title1\n"+
                   "## Section1.1\n"+
                   "### Section1.1.1"]
        html = from_source_tree_to_markdown(sources)
        self.assertNotIn("1.1.1 Section1.1.1", html)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()