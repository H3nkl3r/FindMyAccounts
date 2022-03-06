from setuptools import setup
from os.path import dirname, join


def read_file(filename):
    with open(join(dirname(__file__), filename)) as f:
        return f.read()


setup(
    name='WhereDoIHaveAnAccount',
    version='1.0.0',
    packages=['WhereDoIHaveAnAccount'],
    url='https://github.com/H3nkl3r/WhereDoIHaveAnAccount',
    license='AGPL',
    author='Timo Kühne',
    author_email='',
    description='Simple tool to find out where you have accounts',
    install_requires=read_file("requirements.txt").split("\n"),
    extras_require={
        'testing': read_file("requirements_dev.txt").split("\n")
    },
    entry_points={
        'console_scripts': ['WhereDoIHaveAnAccount=WhereDoIHaveAnAccount.scraper:main'],
    },
    include_package_data=True
)
