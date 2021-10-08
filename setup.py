import versioneer
from setuptools import find_packages, setup

import archapp

with open("requirements.txt", "rt") as fp:
    install_requires = [
        line for line in fp.read().splitlines()
        if line and not line.startswith("#")
    ]


setup(
    name='archapp',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license="BSD",
    include_package_data=True,
    packages=find_packages(),
    description='Archiver Appliance Python Interface',
    author='Zachary Lentz',
    author_email='zlentz@slac.stanford.edu',
    install_requires=install_requires,
    python_requires=">=3.6",
)
