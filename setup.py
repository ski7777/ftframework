from setuptools import setup, find_packages

setup(name='ftframework',
      description='A simple framework for multi-client fischertechnik constructions',
      version='1.0.0',
      author='Raphael Jacob',
      author_email='r.jacob2002@gmail.com',
      url='https://github.com/ski7777/ftframework',
      license='GPLv3',
      packages=find_packages(),
      scripts=['ftframework/bin/ftFrameworkClient.py']
      )
