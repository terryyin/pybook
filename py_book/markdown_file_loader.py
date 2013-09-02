'''
All the file operations.
'''


__all__ = ["load_folder"]

import os
import codecs


def _compare_filename(a, b):
    return (a > b) - (a < b) if a.startswith('_') == b.startswith('_') else [1, -1][a.startswith('_')]


_sort_dir_entries = lambda direntries: direntries.sort(cmp=_compare_filename)
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
    _sort_dir_entries = lambda direntries: direntries.sort(key=cmp_to_key(_compare_filename))


def load_folder(pathnames):
    for pathname in pathnames:
        if os.path.isfile(pathname):
            with codecs.open(pathname, 'r', encoding="utf-8") as md_file:
                yield md_file.read()
        else:
            direntries = os.listdir(pathname)
            _sort_dir_entries(direntries)
            yield load_folder(os.path.join(pathname, entry) for entry in direntries)
