'''
'''

__all__ = ["from_source_tree_to_markdown"]

try:
    import markdown
except:
    print ("You need to install Python markdown module.")
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

