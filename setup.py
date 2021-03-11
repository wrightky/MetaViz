import setuptools
from MetaViz import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MetaViz",
    version=__version__,
    license='MIT',
    author="Kyle Wright",
    author_email="kyleawright@utexas.edu",
    description="Search and visualize metadata information for photo and video collections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wrightky/MetaViz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"],
    install_requires = ['numpy','matplotlib','pandas'],
    keywords=['metadata', 'visualization', 'photos', 'archive']
)
