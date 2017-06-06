from distutils.core import setup
import archapp

setup(name='archapp', version=archapp.__version__, packages=['archapp'],
      description='Archiver Appliance Python Interface',
      author='Zachary Lentz', author_email='zlentz@slac.stanford.edu')
