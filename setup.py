from setuptools import setup
setup(name='selenium_scraper',
    version='0.0.1',
    description='A Selenium Scraper Class',
    author='Marc Inizan',
    author_email='locstaw@gmail.com',
    packages=['selenium_scraper'],
    install_requires=['selenium', 'logging', 'datetime', 'os', 're', 'pandas'])