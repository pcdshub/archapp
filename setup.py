from setuptools import setup, find_packages
import archapp

setup(
    name='archapp',
    version=archapp.__version__,
    #packages=['archapp'],
    packages=find_packages(),
    description='Archiver Appliance Python Interface',
    author='Zachary Lentz',
    author_email='zlentz@slac.stanford.edu'
)
