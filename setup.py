from setuptools import setup
import pypandoc

try:
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(name='preseeapy',
      version='1.2',
      description='Corpus data processing for PRESEEA',
      long_description=long_description,
      packages=['preseeapy'],
      author = 'Pablo Oberm',
      author_email = 'paul.pauuul@gmail.com',
      package_data={'': ['*.json', '*.cfg']},
      zip_safe=False)