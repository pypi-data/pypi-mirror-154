import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name="pysmithplot_3.10",
      version="0.2.0",
      packages=["smithplot"],
      description="An extension for Matplotlib providing a projection class to generate high quality Smith Chart plots.",
      long_description=read('README.md'),
      author="Mario Krattenmacher",
      author_email="Mario.Krattenmacher@semimod.de",
      license="BSD",
      url="https://github.com/miesli/pySmithPlot",
      install_requires=["matplotlib >= 1.2.0", "numpy", "scipy"])
