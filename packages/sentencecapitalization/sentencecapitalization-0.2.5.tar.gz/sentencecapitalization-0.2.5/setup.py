from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.2.5'
DESCRIPTION = 'capitalizing full string'
LONG_DESCRIPTION = 'capitalization of string having multiple words'

# Setting up
setup(
    name="sentencecapitalization",
    version=VERSION,
    author="vijay_59 (vijaysinghbhadoriya592@gmail.com)",
    author_email="vijaysinghbhadoriya592@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    py_modules=["CapitalizeFullString"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)