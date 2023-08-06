from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pySummarizedExperiment',
    version='0.1.0',    
    description="A Python port of R's SummarizedExperiment package",
    url='https://github.com/Pascallio/pySummarizedExperiment',
    author='Pascal Maas',
    author_email='p.maas92@gmail.com',
    license='Apache-2.0',
    packages=['pySummarizedExperiment'],
    install_requires=['pandas',
                      'numpy',                     
                      ],
    long_description=long_description,
    long_description_content_type='text/markdown',

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.9',
    ],
)
