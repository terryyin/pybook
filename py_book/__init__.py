'''
To be added
'''

VERSION = "0.0.2"

import markdown

def toHTML(pathname):
    ''' Convert a folder or a md file into HTML.
    '''
    with open(pathname, 'r') as f:
        return markdown.markdown(f.read())


