![metaviz logo](https://github.com/wrightky/MetaViz/blob/main/gallery/banner.gif)

# MetaViz - Media Metadata Visualization Library

**Repository of tools to interface with, visualize, and edit the metadata information in a collection or archive of visual media (i.e. photos and videos).**

Codes and tools in this repository are all built in Python -- however, for metadata access, we require a local installation of the free perl library [exiftool](https://exiftool.org/). All interfacing between this library and exiftool is done through the bash shell, so this is not a sophisticated Python wrapper for any of the exiftool functionality. Rather, these tools are secondary, surface-layer codes which provide an easy way to interface with the metadata in a collection of visual media. This repository includes functions to find files whose metadata match certain search criteria, and tons of good looking, ready-to-use plotting routines for visualizing that information.

To keep all these functions quick, we keep the exiftool calls to a minimum by saving most of the metadata information in a directory of `.csv` files, and rely on `Pandas` for most of the direct processing. For plotting, we require at least an installation of `matplotlib`, with many optional functions based in other libraries like `seaborn`, `networkx`, and `chord`. My goal is that the aesthetic adjustments made behind the scenes in the plotting routines will provide nice, good-looking visualizations right out of the box.

Examples of these visualizations can be seen below, and in the examples folder.

If you have any suggestions or requests for visualizations that would better suit your data, please feel free to reach out or open an issue, and I will gladly try to help!
