from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Random Name Generator'
LONG_DESCRIPTION = 'Generates random male names'

# setup
setup(
    name="namegeneratormodule",
    version=VERSION,
    author="Nuke",
    author_email="rochadcmarcos@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],

    keywords=['python', 'first packages'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)