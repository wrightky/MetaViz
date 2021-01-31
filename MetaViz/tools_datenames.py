#!/usr/bin/env python3
"""
Tools designed specifically for collections whose
filenames are datetime strings
"""
import os
import pandas as pd


def Dates2Names(folder, dt_format='%Y%m%d_%H%M%S',
                datesource='CreateDate'):
    """
    Send datetimes from the metadata field datesource into
    the filenames of the sourcefiles in the specified folder,
    according to the exiftool format specified
    
    Inputs:
        folder (str) : Folder in which to update filenames
        dt_format (str) : Datetime format to use in the exiftool call
        datesource (str) : Metadate field from which to grab the dates,
            e.g. CreateDate or FileModifyDate
    Outputs:
        Updates the filenames in folder using exiftool
    """
    # Run exiftool through bash shell command
    cmd = ('exiftool -d %s%%%%-c.%%%%e "-filename<%s" %s' % (dt_format,
                                                             datesource,
                                                             folder))
    os.system(cmd) # Run
    return


def Names2Dates(csvName,
                datefields=['CreateDate','FileModifyDate'],
                dt_format = '%Y%m%d_%H%M%S'):
    """
    Function to update the csv metadata date fields using
    the date specified in the filename. Note that function
    does not actually run exiftool, only propagates the
    information into the csv file.
    
    Inputs:
        csvName (str) : Path to csv in which to update metadata
        datefields (list) : List of which date-related metadata
            fields to update
        dt_format (str) : Datetime format matching oldDates, given
            as one of the formats recognized by pandas.to_datetime()
    """
    # Using pandas on a previous exiftool call
    df = pd.read_csv(csvName, encoding="ISO-8859-1")

    # Read in filenames to get 'corrected' datetime
    fileNames = df['SourceFile'].values.tolist()
    # Make sure to eliminate path and extensions
    fileNames = [f.split(os.sep)[-1] for f in fileNames]
    fileNames = [f.split('.')[0] for f in fileNames]
    
    # Use pandas to auto-reformat date
    df2 = pd.DataFrame()
    df2['NameDates'] = pd.to_datetime(fileNames, format=dt_format)
    dates = df2['NameDates'].dt.strftime('%Y:%m:%d %H:%M:%S').tolist()
    
    # Update fields in CSV
    for field in datefields:
        df[field] = dates
    
    # Re-save CSV
    df.to_csv(csvName, index=False, encoding = "ISO-8859-1")
    return