#!/usr/bin/env python3
"""
Misc additional tools that may be useful for the archive
"""
import os
# import cv2
# import shutil


def CopyFiles(sourcefiles, dst_folder):
    """
    Copy a list of sourcefiles to a destination folder.
    
    Inputs:
        sourcefiles (list) : List of paths to sourcefiles to copy,
            specified as stringss, e.g. the output of 
            Archive.FindSource([...], withPath=True)
        dst_folder (str) : Destination folder to which to copy
    Outputs:
        Copies each sourcefile to the specified folder
    """
    import shutil

    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    for name in sourcefiles:
        shutil.copy2(name, os.path.join(dst_folder,
                                        name.split(os.sep)[-1]))
    return


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
    return
