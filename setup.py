from setuptools import setup


setup(name='preseeapy',
      version='1.1',
      description='Corpus data processing for PRESEEA',
      packages=['preseeapy'],
      author = 'Pablo Oberm',
      author_email = 'paul.pauuul@gmail.com',
      package_data={'': ['*.json', '*.cfg']},
      zip_safe=False)