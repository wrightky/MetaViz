#!/usr/bin/env python3
"""
Plotting routines dedicated to previewing images
"""
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# from PIL import Image
from . import config as cf

#--------------------------------------
# Image Plots
#--------------------------------------
def ShowThumbnails(files, res=64, showTitle=True, size='x-small'):
    """
    Generate a plot of image thumbnails for a given list of files.
    Expects files to include the full path to the image.
    
    Note: Function requires a functional installation of Pillow
    Inputs:
        files (list) : List of paths to image files to show
        res (int) : Resolution of the resized thumbnails, wherein
            the max size is an image of size (res, res)
        showTitle (bool) : Optionally show filename thumbnail titles
        size (str) : Text size to be used if showTitle==True, needs
            to be string recognized by matplotlib function ax.set_text()
    """
    # Check if Chord is available
    if not cf.PillowAvailable:
        print("Function unavailable, requires installation of Pillow")
        print("See installation guide for auxilary packages")
        return
    from PIL import Image
    
    titles = [os.path.basename(m).split('.')[0] for m in files]

    # Subplot dimensions
    N = len(files)
    cols = int(np.ceil(N**0.5))
    rows = int(np.ceil(N/cols))

    # Create a Position index
    position = list(range(1, N+1))

    # Plot thumbnails
    fig = plt.figure(1, figsize=(5,5), dpi=200)
    for k in list(range(N)):
        # Load image with pillow
        try:
            im = Image.open(files[k])
        except:
            print('Warning: Some files listed may not be images. Skipping')
            continue
        im.thumbnail((res, res), Image.ANTIALIAS) # resize image in-place

        ax = fig.add_subplot(rows, cols, position[k])
        implot = ax.imshow(im)
        ax.set_xticks([])
        ax.set_yticks([])
        if showTitle:
            ax.set_title(titles[k], size=size)
    plt.show()
    return