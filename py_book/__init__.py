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
import types
from .markdown_extensions import PybookMarkdownExtension


def _is_node(sources):
    try:
        return isinstance(sources, types.StringTypes)
    except AttributeError:
        return isinstance(sources, str)

def _from_source_tree_to_markdown_with_session(sources, md):
    if _is_node(sources):
        return md.convert(sources)
    return '\n'.join(_from_source_tree_to_markdown_with_session(source, md) for source in sources)

def from_source_tree_to_markdown(sources):
    md = markdown.Markdown(extensions = ['meta', PybookMarkdownExtension()])
    return _from_source_tree_to_markdown_with_session(sources, md)


def _compare_filename(a, b):
    return (a > b) - (a < b) if a.startswith('_') == b.startswith('_') else [1, -1][a.startswith('_')]


_sort_dir_entries = lambda(direntries): direntries.sort(cmp=_compare_filename)
try:
    # Python 2.x?
    _sort_dir_entries([])
except:
    # Python 3
    def cmp_to_key(mycmp):
        'Convert a cmp= function into a key= function'
        class K(object):
            def __init__(self, obj, *args):
                self.obj = obj
            def __lt__(self, other):
                return mycmp(self.obj, other.obj) < 0
            def __gt__(self, other):
                return mycmp(self.obj, other.obj) > 0
            def __eq__(self, other):
                return mycmp(self.obj, other.obj) == 0
            def __le__(self, other):
                return mycmp(self.obj, other.obj) <= 0  
            def __ge__(self, other):
                return mycmp(self.obj, other.obj) >= 0
            def __ne__(self, other):
                return mycmp(self.obj, other.obj) != 0
        return K
    _sort_dir_entries = lambda(direntries): direntries.sort(key=cmp_to_key(_compare_filename))


def load_folder(pathnames):
    for pathname in pathnames:
        if os.path.isfile(pathname):
            with codecs.open(pathname, 'r', encoding="utf-8") as md_file:
                yield md_file.read()
        else:
            direntries = os.listdir(pathname)
            _sort_dir_entries(direntries)
            yield load_folder(os.path.join(pathname, entry) for entry in direntries)


def to_html(pathname):
    ''' Convert a folder or a md file into HTML.
    '''
    sources = load_folder([pathname])
    return from_source_tree_to_markdown(sources)


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
