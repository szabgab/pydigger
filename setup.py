from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pydigger',
      version='0.1',
      description='Diggin Py',
      long_description=readme(),
      url='http://github.com/szabgab/pydigger',
      author='Gabor Szabo',
      author_email='gabor@szabgab.com',
      license='MIT',
      packages=['pydigger'],
      requires=[
          'urllib2',
          'feedparser',
          #'pkg_resources',
      ],
      tests_require=[
          'nose',
      ],
      test_suite='nose.collector',
      scripts=['bin/pydigger'],
      zip_safe=False)

