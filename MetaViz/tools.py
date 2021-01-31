#!/usr/bin/env python3
"""
Misc additional tools that may be useful for the archive
"""
import numpy as np
import os
# import pandas
# import cv2
# import shutil

def StitchPan(images, outfile, mode=1):
    """
    Automatically stitches together panoramic photos from
    sub-scenes or scans. Requires cv2
    
    Inputs:
        images (list) : List of absolute or relative paths to images
            to be stitched together, specified as strings
        outfile (str) : Output filename and path to save panoramic
        mode (int) : Mode used as input to cv2.Stitcher.create(),
            defaults to 1 for scanned (flat) photos
    Outputs:
        Saves output panoramic photo, if stitching is successful
    """
    try:
        import cv2
    except ImportError:
        print("Cannot stitch panoramic, requires installation of cv2")
        return

    # read input images
    imgs = []
    for img_name in images:
        img = cv2.imread(cv2.samples.findFile(img_name))
        if img is None:
            print("Can't read image " + img_name)
            break
        imgs.append(img)

    stitcher = cv2.Stitcher.create(mode)
    status, pano = stitcher.stitch(imgs)

    if status != cv2.Stitcher_OK:
        print("Can't stitch images, error code = %d" % status)
    else:
        cv2.imwrite(outfile, pano)
        print("Stitching successful, %s saved" % output_file)