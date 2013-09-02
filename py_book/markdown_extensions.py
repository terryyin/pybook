'''
'''

try:
    import markdown
except:
    print ("You need to install Python markdown module.")



def embed_value(name):
    return "{%s}" % name


class SectionCounter(object):
    '''
    Count the chapter and sessions.
    '''
    
    def __init__(self):
        self.section_ids = ['0']
        self.next_chapter = None

    
    def next_section(self, level):
        if level == 1 and self.next_chapter:
            self.section_ids = [self.next_chapter]
            self.next_chapter = None
            return
        self.section_ids.extend(['0'] * (level - len(self.section_ids)))
        self.section_ids = self.section_ids[:level]
        self.section_ids[level - 1] = self._get_next_id(self.section_ids[level - 1])
    

    def _get_next_id(self, next_chapter_id):
        try:
            return str(int(next_chapter_id) + 1)
        except ValueError:
            return chr(ord(next_chapter_id) + 1)

    
    def get_id(self, level):
        return '.'.join(self.section_ids[:level])

    
    def set_next_chapter(self, next_chapter):
        self.next_chapter = next_chapter


class ChapterTreeprocessor(markdown.treeprocessors.Treeprocessor):

    def __init__(self):
        self.chapter_prefix = None
        self.section_level = 0
        self.section_counter = SectionCounter()


    def run(self, doc):
        self.chapter_prefix = self._get_meta("chapter_prefix", self.chapter_prefix)
        self.section_counter.set_next_chapter(self._get_meta("next_chapter_id", None))
        self.section_level = int(self._get_meta("section_level", self.section_level))
        for elem in doc.getiterator():
            if elem.tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                level = int(elem.tag[-1])
                self.section_counter.next_section(level)
                if level == 1 and self.chapter_prefix:
                    elem.text = "%s %s" % (
                                           self.chapter_prefix.replace(embed_value('chapter_id'), 
                                                                       self.section_counter.get_id(1)), elem.text)
                elif self.section_level >= level:
                    elem.text = "%s %s" % (self.section_counter.get_id(level), elem.text)

                    
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

