from setuptools import setup, find_packages
import codecs, os

VERSION = '1'
DESCRIPTION = 'A basic morse translator'

setup(
  name = 'basic-fast-morse-translator',
  version = VERSION,
  author = "Name",
  author_email = "not_name47@protonmail.com",
  install_requires=[],
  keywords = ['python', 'translation', 'fast', 'morse', 'futuristic'],
  classifiers = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 2',
    'Natural Language :: English',
    'Operating System :: OS Independent'
  ],
  long_description=open('readme.md', 'r').read(),
  long_description_content_type='text/markdown'
)