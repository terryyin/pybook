'''
'''

try:
    import markdown
except:
    print ("You need to install Python markdown module.")



def embed_value(name):
    return "{%s}" % name


class ChapterTreeprocessor(markdown.treeprocessors.Treeprocessor):

    def __init__(self):
        self.start_level = 0
        self.chapter_prefix = None
        self.chapter_count = '1'

    def _get_next_chapter(self, chapter_count):
        try:
            return str(int(chapter_count) + 1)
        except ValueError:
            return chr(ord(chapter_count) + 1)
    
    
    def run(self, doc):
        self.start_level = int(self._get_meta("start_level", self.start_level + 1)) - 1
        self.chapter_prefix = self._get_meta("chapter_prefix", self.chapter_prefix)
        self.chapter_count = self._get_meta("chapter_count", self.chapter_count)
        for elem in doc.getiterator():
            if elem.tag == 'h1':
                if self.chapter_prefix:
                    elem.text = "%s %s" % (self.chapter_prefix.replace(embed_value('chapter_count'), self.chapter_count), elem.text)
                self.chapter_count = self._get_next_chapter(self.chapter_count)
                if self.start_level:
                    level = int(elem.tag[-1]) + self.start_level
                    if level > 6:
                        level = 6
                    elem.tag = 'h%d' % level
                    
    def _get_meta(self, name, default = None):
        if hasattr(self.md, 'Meta'):
            if name in self.md.Meta:
                return self.md.Meta[name][0]
        return default

class PybookMarkdownExtension(markdown.Extension):

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        self.processor = ChapterTreeprocessor()
        self.processor.md = md
        self.processor.config = self.getConfigs()
        md.treeprocessors.add('chapters', self.processor, '_end')

