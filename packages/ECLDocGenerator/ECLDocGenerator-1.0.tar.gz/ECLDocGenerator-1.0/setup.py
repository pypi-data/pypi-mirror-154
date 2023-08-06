from setuptools import setup, find_packages

import os

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('src/ecldoc/Templates')

setup(
    name="ECLDocGenerator",
    version="1.0",
    packages=find_packages(),
    install_requires=['Jinja2==2.9.6', 'lxml==3.8.0'],
    license='BSD',
    author=u'Shivam Singhal',
    author_email='shivams2799@gmail.com',
    package_data={'': extra_files},
    scripts=['src/bin/ecldoc'],
    platforms='Linux',
    url="https://github.com/championshuttler/ECLDocGenerator",
    download_url='https://pypi.python.org/pypi/ECLDocGenerator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    )
