import os.path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='ap-precinct-parser',
    version='0.2',
    author='Annie Daniel, Jeremy Bowers',
    author_email='annie.daniel@nytimes.com, jeremy.bowers@nytimes.com',
    url='https://github.com/newsdev/ap-precinct-parser',
    description='Client for parsing the Associated Press\'s precinct results file over FTP',
    long_description=read('README.md'),
    packages=['apftp',],
    entry_points={
        'console_scripts': (
            'apftp = apftp.precincts:main',
        ),
    },
    license="Apache License 2.0",
    keywords='election race candidate democracy news associated press',
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ]
)
