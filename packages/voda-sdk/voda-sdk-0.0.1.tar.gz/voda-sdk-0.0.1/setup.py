import os
import sys

from setuptools import setup, find_packages


__version__ = '0.0.1'
__author__ = 'Yeongbin Jo <yeongbin.jo@vodavision.ai>'


with open('README.md') as readme_file:
    long_description = readme_file.read()


# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()
elif sys.argv[-1] == 'clean':
    import shutil
    if os.path.isdir('build'):
        shutil.rmtree('build')
    if os.path.isdir('dist'):
        shutil.rmtree('dist')
    if os.path.isdir('voda_sdk.egg-info'):
        shutil.rmtree('voda_sdk.egg-info')


setup(
    name="voda-sdk",
    version=__version__,
    author="Yeongbin Jo",
    author_email="yeongbin.jo@vodavision.ai",
    description="Software development kit for VODA AI Service (https://vodavision.ai)",
    license="MIT",
    keywords="python",
    url="https://github.com/VODA-VISION-AI/voda-sdk-python",
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    long_description_content_type='text/markdown',
    long_description=long_description,
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Installation/Setup',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)