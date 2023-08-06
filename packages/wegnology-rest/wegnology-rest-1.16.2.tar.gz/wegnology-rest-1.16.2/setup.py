from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wegnology-rest',
    version='1.16.2',
    description='A REST client for the WEGnology API',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://github.com/WEGnology/wegnology-rest-python',
    author='WEGnology',
    author_email='hello@wegnology.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Topic :: Communications',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    keywords=['REST', 'WEGnology', 'IoT'],
    test_suite='tests',
    install_requires=['requests>=2.13'],
    tests_require=['requests-mock>=1.9.0'],
)
