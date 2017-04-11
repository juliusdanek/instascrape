from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='instascrape',
      version='0.1',
      description='Instagram Scraper written in Python. Mainly able to scrape # of followers, email addresses and biographies for now',
      url='https://github.com/juliusdanek/instascrape',
      keywords='instagram scraper python biography',
      author='Julius Danek',
      author_email='juliusdanek@gmail.com',
      license='MIT',
      packages=['instascrape'],
      install_requires=[
          'validate_email',
          'requests',
          'lxml'
      ],
      zip_safe=False)
