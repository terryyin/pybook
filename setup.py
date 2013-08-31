#!/usr/bin/env python
# encoding: utf-8
'''
'''
import py_book
from distutils.core import setup
def install():
    try:
        long_description = open("README.md").read()
    except:
        long_description = py_book.__doc__    
    setup(
          name = 'pybook',
          version = py_book.VERSION,
          description =  py_book.__doc__, 
          long_description =  long_description,
          url = 'https://github.com/terryyin/pybook',
          classifiers = ['Development Status :: 1 - Planning',
                     'Intended Audience :: End Users/Desktop',
                     'License :: Freeware',
                     'Operating System :: POSIX',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: MacOS :: MacOS X',
                     'Topic :: Software Development :: Quality Assurance',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 2.6',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3.2',
                     'Programming Language :: Python :: 3.3'],
          package_dir = {'pybook':'py_book'},
          packages = ['pybook'],
          install_requires=['markdown'],
          author = 'Terry Yin',
          author_email = 'terry@odd-e.com',
          scripts=['pybook']
          )

if __name__ == "__main__":
    install()
