from setuptools import setup, find_packages
from distutils.util import convert_path

with open("README.md") as f:
    readme = f.read()

with open("requirements.txt") as f:
    requirements = f.read().split()

main_ns = {}
ver_path = convert_path('tar_dir_indexer/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name='tar_dir_indexer',
    version=main_ns['__version__'],
    packages=find_packages(),
    url='https://github.com/CeadeS/tar_dir_indexer',
    license='BSD-3-Clause License',
    author='Martin Hofmann',
    author_email='Martin.Hofmann@tu-ilmenau.de',
    description='Indexes directories unraveling tar files within. Also indexes nested tar files.',
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
