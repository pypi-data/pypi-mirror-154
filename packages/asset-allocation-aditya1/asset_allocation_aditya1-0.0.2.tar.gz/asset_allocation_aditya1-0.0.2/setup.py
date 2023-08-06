from setuptools import setup, find_packages

classifiers = [
'Development Status :: 5 - Production/Stable',
'Intended Audience :: Education',
'Operating System :: Microsoft :: Windows :: Windows 10',
'License :: OSI Approved :: MIT License',
'Programming Language :: Python :: 3'

]

setup (
name= 'asset_allocation_aditya1',
version = '0.0.2',
description= 'Package to draw efficient frontier and study portfolio performance',
long_description= open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(), 
url = '',
author = 'Aditya Saha',
author_email= 'adityaranjha786@gmail.com',
license='MIT',
classifiers= classifiers,
keywords= 'Efficient Frontier',
packages = find_packages('asset_allocation'),
install_requires= ['pandas_datareader', 'numpy', 'plotly', 'datetime', 'scipy']
)
