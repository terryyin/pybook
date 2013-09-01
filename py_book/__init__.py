'''
To be added
'''

VERSION = "0.0.2"

try:
    import markdown
except:
    print ("You need to install Python markdown module.")
import os


def to_html(pathname):
    ''' Convert a folder or a md file into HTML.
    '''
    if os.path.isfile(pathname):
        with open(pathname, 'r') as md_file:
            return markdown.markdown(md_file.read())
    direntries = os.listdir(pathname)
    direntries.sort()
    return '\n'.join(to_html(os.path.join(pathname, entry)) for entry in direntries)


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
    print (to_html(args[1]))
