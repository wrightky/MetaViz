#!/usr/bin/env python3
"""
Misc additional tools that may be useful for the archive
"""
import os
import pandas as pd
import numpy as np
import re
# import cv2
# import shutil

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
            specified as strings, e.g. the output of 
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
    # Check if OpenCV is available
    try:
        import cv2
    except ImportError:
        print("Function unavailable, requires installation of OpenCV")
        print("Perform full setup for auxilary packages")
        return

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


def Coverage2Coords(archive, geolocator, min_delay_seconds=2):
    """
    Using GeoPy geolocator, try to convert Location names in
    the Coverage field to lat/long coordinates. Requires that
    Archive.DownloadCoverage() has been called prior to this
    function. Built around the example provided at
    https://geopy.readthedocs.io/en/latest/#usage-with-pandas
    
    NOTE: Function is not perfect, and almost certainly will
    require manual cleaning after the fact! However, can
    definitely save time for large queries. Make sure that
    usage of this function abides by ToS agreed to by the
    user in obtaining the API key for the GeoPy geolocator
    (e.g. set min_delay_seconds accordingly)
    
    Inputs:
        archive (obj) : archive.Archive() object used to access
            csv files
        geolocator (obj) : A geolocator instance of one of
            the classes inside geopy.geocoders, such as
            OpenMapQuest(api_key = 'user_api_key_here')
        min_delay_seconds (float) : Time delay fed into the
            geopy.extra.rate_limiter.RateLimiter to keep
            repeated queries from overloading the servers and
            violating the user's ToS with the geocoding service
    Outputs:
        Updates the LocationCoords.csv file with coordinates
            for each Location found using a GeoPy search
    """
    # Check if GeoPy is available
    try:
        from geopy.extra.rate_limiter import RateLimiter
    except ImportError:
        print("Function unavailable, requires installation of GeoPy")
        print("Perform full setup for auxilary packages")
        return

    # Set a rate limiter by default to keep within geolocator ToS
    geocode = RateLimiter(geolocator.geocode,
                          min_delay_seconds=min_delay_seconds)
    
    # Load in csv of coverage
    csvname = os.path.join(archive.csvPath, 'LocationCoords.csv')
    if not os.path.exists(csvname):
        print('Error: Archive.DownloadCoverage() must be run '+\
              'before calling this function. Exiting')
        return
    df = pd.read_csv(csvname, encoding = "ISO-8859-1",
                     low_memory=False)
    
    # Call GeoPy geocode function on the Location field of df
    df['Details'] = df['Location'].apply(geocode)
    df['Coord'] = df['Details'].apply(lambda loc: tuple(loc.point) if loc else None)
    
    # Sometimes default XMP syntax is bad for searches.
    # For queries which failed, try again with simplified syntax
    # Create sub-df of modified names, eliminate parenthetical
    df['LocationMod'] = df['Location'].str.replace(r'\([^()]*\)', '')
    df2 = df.loc[df['Coord'].isnull(), ['LocationMod']]

    # Feed sub-df back into geocode
    df2['Details'] = df2['LocationMod'].apply(geocode)
    df2['Coord'] = df2['Details'].apply(lambda loc: tuple(loc.point) if loc else None)
    
    # Update original df with new data
    df.update(df2) 

    # Fix any remaining nulls in coordinates column with (0, 0, 0)
    df2 = df.loc[df['Coord'].isnull(), ['Location']]
    df2['Coord'] = [(0, 0, 0)] * len(df2)
    df.update(df2) 

    # Extract lat long from Coord
    coord = df['Coord'].tolist()
    lat = [p[0] for p in coord]
    lon = [p[1] for p in coord]

    df['Latitude'] = lat
    df['Longitude'] = lon

    # Delete extra columns no longer needed
    df.drop(columns=['LocationMod', 'Coord'], inplace=True)

    # Query often returns complex characters, revert to default encoding
    df = df.applymap(lambda x: str(x).encode("ISO-8859-1",
             errors="ignore").decode("ISO-8859-1", errors="ignore"))
    # Save csv
    df.to_csv(csvname, index=False, encoding="ISO-8859-1")
    return