from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='instascrape',
      version='0.3',
      description='Instagram Scraper written in Python. Mainly able to scrape # of followers, email addresses and biographies for now',
      url='https://github.com/juliusdanek/instascrape',
      download_url='https://github.com/juliusdanek/instascrape/archive/0.1.tar.gz',
      keywords=['instagram', 'scraper', 'python', 'biography'],
      author='Julius Danek',
      author_email='juliusdanek@gmail.com',
      license='MIT',
      packages=['instascrape'],
      install_requires=[
          'validate_email',
          'requests',
          'lxml'
      ])
