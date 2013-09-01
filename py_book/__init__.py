'''
To be added
'''

VERSION = "0.0.2"


def toHTML(pathname):
    ''' Convert a folder or a md file into HTML.
    '''
    import markdown
    with open(pathname, 'r') as f:
        return markdown.markdown(f.read())


