from setuptools import setup


setup(
    name='pydownloader-01',
    version='0.0.2',
    author='Mohammad Alidoust',
    author_email='phymalidoust@gmail.com',
    # packages=['requests', 'bs4', 're', 'urllib'],
    scripts=['pydownloader.py','scraper.py'],
    url='http://mohammad-alidoust.blogspot.com',
    license='LICENSE.txt',
    description='This package extracts all available pdf files from an address.',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    # install_requires=['requests', 'bs4', 're', 'urllib3'],
)
