import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(setup_requires=['wheel'],
      name="DSC_NSD_TEST",
      version="0.0.1",
      description="pytorch implementation of DICE loss",
      long_description=README,
      long_description_content_type="text/markdown",
      url="https://github.com/gc-js/test",
      author="Cheng Ge",
      author_email="13851520957@163.com",
      license="MIT",
      classifiers=["License :: OSI Approved :: MIT License",
                   "Programming Language :: Python :: 3.6",
                   "Programming Language :: Python :: 3.9"],
      packages=["DSC_NSD_TEST"],
      install_requires=["nibabel"])