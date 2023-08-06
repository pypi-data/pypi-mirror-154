from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='disentpy',
    version='0.0.7',
    description='Disent API caller',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/disentcorp/disentpy',
    author='Niels lauritzen',
    author_email='niels.lauritzen@disent.com',
    license_files = ('LICENSE.md',),
    packages=['disent'],
    install_requires=['requests'],
    zip_safe=False
)