import sys
import os
import re
from setuptools import setup, find_packages


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


requires = [
    'futures',
    'pathlib2',
    'Plim',
    'tornado',
]

with open('quip/__init__.py') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

with open('README.rst') as fd:
    readme = fd.read()


setup(
    name='quip',
    version=version,
    description='Simple web interface framework for command-line applications.',
    long_description=readme,
    author='Feihong Hsu',
    author_email='feihong.hsu@gmail.com',
    url='https://github.com/feihong/quip',
    packages=find_packages(),
    package_data={'': '*.html'},
    install_requires=requires,
    license='Apache 2.0',
    zip_safe=False,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ),
)
