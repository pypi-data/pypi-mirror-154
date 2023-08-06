"""Instalador para el paquete "passwordCracker"."""

from setuptools import setup

long_description = (
    open('README.txt').read()
    + '\n' +
    open('LICENSE').read()
    + '\n')

setup(
    name="passwordCracker",
    version="1.1",
    description="A tool to perform a dictionary attack to OS hashes file.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        # Indica la estabilidad del proyecto. Los valores comunes son
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indique a quien va dirigido su proyecto
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography",
        # Indique licencia usada (debe coincidir con el "license")
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        # Indique versiones soportas, Python 2, Python 3 o ambos.
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords="cybersecurity cracking dictionary attack passwords OS",
    author="Cristina Galván",
    author_email="cristina.galvan.prieto@hotmail.com",
    license="GNU GPLv3",
    packages=["passwordCracker"]
)
