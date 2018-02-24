import ast
import re
from setuptools import setup


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('courier/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(
    name='courier',
    author='v1c77',
    author_email='heyuhuade@gmail.com',
    version=version,
    url='https://github.com/v1c77/kindle-courier',
    packages=['courier'],
    description='A courier CLI focus on send book to kindle.',
    classifiers=[
        'license :: OSI Approved :: WTFPL License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    entry_points='''
        [console_scripts]
        courier=courier.cli:cli
    '''
)
