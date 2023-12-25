try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(name='moonshot',
      use_scm_version=True,
      setup_requires=['setuptools_scm'],
      version='1.0',
      description='crater detection software',
      author='ACSE project',
      packages=['Moonshot','moon_dataset_maker']
      )