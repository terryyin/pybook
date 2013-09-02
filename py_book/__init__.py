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



def is_node(sources):
    try:
        return isinstance(sources, types.StringTypes)
    except AttributeError:
        return isinstance(sources, str)

def _from_source_tree_to_markdown_with_session(sources, md):
    if is_node(sources):
        return md.convert(sources)
    return '\n'.join(_from_source_tree_to_markdown_with_session(source, md) for source in sources)

def from_source_tree_to_markdown(sources):
    md = markdown.Markdown(extensions = ['meta', PybookMarkdownExtension()])
    return _from_source_tree_to_markdown_with_session(sources, md)


def _compare_filename(a, b):
    return cmp(a, b) if a.startswith('_') == b.startswith('_') else [1, -1][a.startswith('_')]


def load_folder(pathnames):
    for pathname in pathnames:
        if os.path.isfile(pathname):
            with codecs.open(pathname, 'r', encoding="utf-8") as md_file:
                yield md_file.read()
        else:
            direntries = os.listdir(pathname)
            direntries.sort(cmp = _compare_filename)
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
