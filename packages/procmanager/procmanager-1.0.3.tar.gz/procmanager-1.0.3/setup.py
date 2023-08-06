from setuptools import setup

setup(
   name='procmanager',
   version='1.0.3',
   description='Helps starting & stopping programs',
   long_description=open('README.md', encoding='utf-8').read(),
   long_description_content_type="text/markdown",
   author='Fabien Devaux',
   url='https://github.com/fdev31/procmanager',
   author_email='fdev31@gmail.com',
   packages=['procmanager'],  # would be the same as name
   scripts=['scripts/procmgr'],
   )
