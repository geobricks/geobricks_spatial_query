from setuptools import setup
from setuptools import find_packages

setup(
    name='GeobricksSpatialQuery',
    version='0.0.6',
    author='Simone Murzilli; Guido Barbaglia',
    author_email='geobrickspy@gmail.com',
    packages=find_packages(),
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    description='Geobricks library to handle spatial queries.',
    install_requires=[
        'flask',
        'flask-cors',
        'simplejson',
        'Geobrickscommon',
        'GeobricksDBMS'
    ],
    url='http://pypi.python.org/pypi/GeobricksSpatialQuery/',
    keywords=['geobricks', 'postgis', 'gis', 'statistics', 'geostatistics', 'spatial', 'spatial query']
)
