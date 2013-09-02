'''
To be added
'''

VERSION = "0.0.2"

from .markdown_file_loader import load_folder
from .tree_markdown import from_source_tree_to_markdown


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
