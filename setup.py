import os
from setuptools import find_packages, setup

__VERSION__ = '0.3.4'

with open('README.md', 'r') as fh:
    long_description = fh.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='AX3 Mercadopago',
    version=__VERSION__,
    packages=find_packages(),
    include_package_data=True,
    description='A Django app to add support for Mercadopago payments',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://github.com/Axiacore/ax3-mercadopago',
    author='Axiacore, ',
    author_email='info@axiacore.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'pymercadopago >= 0.3.0',
        'python-dateutil >= 2.8.1',
        'django >= 2.2.0',
    ],
)
