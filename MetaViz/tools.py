#!/usr/bin/env python3
"""
Misc additional tools that may be useful for the archive
"""
import os
import pandas as pd
# import cv2
# import shutil
from . import config as cf


def IntersectLists(entries):
    """
    Find intersection of input lists. Useful for 
    existing lists or complex searches.

    Inputs:
        entries (list) : list of lists to
            intersect [[...],[...]]
    Outputs:
        intersection (list) : intersection of all entry lists
    """
    for ii in list(range(len(entries)-1)):
        if ii == 0:
            entryset = set(entries[0])
        else:
            entryset = set(intersection)
        intersection = list(entryset.intersection(entries[ii+1]))
    # Re-sort if necessary
    intersection = sorted(intersection)
    return intersection


def DifferenceLists(entries):
    """
    Find difference of one list with another.
    Useful for existing lists or complex searches.

    Inputs:
        entries (list) : list of two lists to
            difference [[...],[...]]
    Outputs:
        diff (list) : difference of all entry lists
    """
    if len(entries) > 2:
        raise ValueError('Symmetric difference only works on two lists')
    entryset = set(entries[0])
    diff = list(entryset.symmetric_difference(entries[1]))
    # Re-sort if necessary
    diff = sorted(diff)
    return diff


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


def BatchRename(oldNames, newNames):
    """
    Rename a list of files given in oldNames to the newName
    of the same index.
    
    Inputs:
        oldNames (list) : List of absolute or relative paths to
            existing files to be renamed
        newNames (list) : List of absolute or relative paths to
            new names for the files in oldNames
    Outputs:
        Changes the name of each file in oldNames to match newNames
    """
    for ii in list(range(0, len(oldNames))):
        # Don't rename a file already in the correct format
        if oldNames[ii] == newNames[ii]:
            continue
        
        # Check if another file of same name as newName exists:
        if not os.path.exists(newNames[ii]):
            os.rename(oldNames[ii], newNames[ii])
        else: # If so, append name with a digit
            suffix = 1
            while True:
                filetype = oldNames[ii].split('.')[-1]
                appendedName = newNames[ii].split('.')[0] + '-' \
                               + str(suffix) + filetype
                if not os.path.exists(appendedName):
                    os.rename(oldNames[ii], appendedName)
                    break
                suffix += 1
    return


def BatchTimedelta(oldDates, timedelta, dt_format='%Y%m%d_%H%M%S'):
    """
    Simple function to take a list of datetimes and add a constant
    time-delta, useful for batch date correction.
    
    Inputs:
        oldDates (list) : List of old datetimes to be fixed
        timedelta (str) : Constant timedelta to add to oldDates,
            specified in a format recognized by pandas.Timedelta(),
            such as "1hr"
        dt_format (str) : Datetime format matching oldDates, given
            as one of the formats recognized by pandas.to_datetime()
    Outputs:
        newDates (list) : List of new datetimes after shift
    """
    df = pd.DataFrame()
    df['oldDates'] = pd.to_datetime(oldDates, format=dt_format)
    df['newDates'] = df['oldDates'] + pd.Timedelta(timedelta)
    newDates = df['newDates'].dt.strftime(dt_format).tolist()
    
    return newDates


def CountUnique(series, delimiter=', '):
    """
    Count unique entries in a column of a pandas series.
    Returns a new DataFrame with unique labels and
    their appearance count.

    Inputs:
        series (pandas series) : Column of a dataframe,
                e.g. df['A']
        delimiter (str) : String delimiter used to
                separate entries in column of interest.
    Outputs:
        uq (pandas DataFrame) : New dataframe containing
                all unique entries and their appearance
                counts, sorted by appearance.
    """
    # Narrow down to unique rows
    entries = series.unique().tolist()
    # Remove nan if necessary
    entries = [x for x in entries if str(x) != 'nan']
    # Join these all into one string
    unique_entries = delimiter.join(name for name in entries)
    # Break string into list at delimiter
    unique_list = unique_entries.split(delimiter)
    unique_list = list(filter(None, unique_list))
    # Remove duplicates
    unique_list = list(dict.fromkeys(unique_list))

    # Create new DataFrame
    uq = pd.DataFrame(unique_list, columns=['Entry'])
    # Count appearances of each entry in original dataframe
    uq['Count'] = uq.apply(lambda row: \
                           np.nansum(series.str.count(\
                           r'%s' % re.escape(row['Entry'])).values),
                           axis=1)
    # Now fix double-counting of entries contained
    # inside other entries
    for ii in uq.index:
        thisname = uq['Entry'][ii]
        for jj in uq.index:
            thatname = uq['Entry'][jj]
            if (thisname in thatname) & (thisname != thatname):
                uq.loc[ii,'Count'] = uq['Count'][ii] \
                                     - uq['Count'][jj]

    uq = uq.sort_values('Count', ascending=False)
    uq.reset_index(drop=True, inplace=True)
    return uq


def StitchPanorama(images, outfile, mode=1):
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
    # Check if Chord is available
    if not cf.OpenCVAvailable:
        print("Function unavailable, requires installation of OpenCV")
        print("See installation guide for auxilary packages")
        return
    import cv2

    # read input images
    imgs = []
    for img_name in images:
        img = cv2.imread(cv2.samples.findFile(img_name))
        if img is None:
            print("Can't read image " + img_name)
            break
        imgs.append(img)

    # Do stitching
    stitcher = cv2.Stitcher.create(mode)
    status, pano = stitcher.stitch(imgs)

    if status != cv2.Stitcher_OK:
        print("Can't stitch images, error code = %d" % status)
    else:
        cv2.imwrite(outfile, pano)
        print("Stitching successful, %s saved" % output_file)
    return
