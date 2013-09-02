'''
To be added
'''

VERSION = "0.0.2"

try:
    import markdown
except:
    print ("You need to install Python markdown module.")
import os
import codecs


class Markdown_Source_Tree(object):
    
    def __init__(self, pathname):
        self.pathname = pathname

    def _is_node(self):
        return os.path.isfile(self.pathname)
    
    def _get_source(self):
        with codecs.open(self.pathname, 'r', encoding="utf-8") as md_file:
            return md_file.read()
    
    def _get_children(self):
        direntries = os.listdir(self.pathname)
        direntries.sort()
        return list(Markdown_Source_Tree(os.path.join(self.pathname, entry)) for entry in direntries)

    def combine_source_tree(self):
        if self._is_node():
            return self._get_source()
        return '\n'.join(child.combine_source_tree() for child in self._get_children())


def to_html(pathname):
    ''' Convert a folder or a md file into HTML.
    '''
    source_tree = Markdown_Source_Tree(pathname)
    return markdown.markdown(source_tree.combine_source_tree())


def create_option_parser():
    from optparse import OptionParser
    parser = OptionParser(version=VERSION)
    parser.usage = '''pybook [options] [PATH or FILE]
                      Or pybook --help'''
    parser.description = __doc__
    return parser


def main():
    import sys
    option_parser = create_option_parser()
    _, args = option_parser.parse_args(args=sys.argv)
    if len(args) < 2:
        return option_parser.print_usage()
    print (to_html(args[1]).encode('utf-8'))
