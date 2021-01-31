#!/usr/bin/env python3
"""
Establish main class for the photo archive/collection
"""
import numpy as np
import pandas as pd
import os
import re
from . import config as cf

class Archive():
    """Parent class for the media collection"""
    def __init__(self):
        # Store details on collection location
        self.CollectionPath = cf.CollectionPath
        self.csvPath = cf.csvPath
        self.BackupPath = cf.BackupPath
        self.subfolders = cf.subfolders
        self.fields = cf.fields
        self.fields_short = cf.fields_short
        
        # Set verbose flag for function printing
        self.verbose = cf.verbose
        
        # Information on packages
        self.SeabornAvailable = cf.SeabornAvailable
        self.ChordAvailable = cf.ChordAvailable
        self.NetworkXAvailable = cf.NetworkXAvailable


    def UpdateCSV(self, subfolders=None):
        """
        For a given list of subfolders, loop through and update the
        exiftool csv for that year. Must be called before later functions
        in this script.

        Inputs:
            subfolders (list) : subfolders to update, default is all
        Outputs:
            Saves new csv files for specified folders in csvPath
        """

        # Check input
        if subfolders is None:
            subfolders = self.subfolders
        elif not isinstance(subfolders, list):
            subfolders = [subfolders]

        for sf in subfolders:
            # Grab absolute path of this subfolder
            foldername = os.path.join(self.CollectionPath, sf)

            # Create a name for csv preserving dir structure
            csvname = os.path.join(self.csvPath,
                                   sf.replace(os.sep,'__') + '.csv')

            # Run exiftool through bash shell command
            bashcmd = ('exiftool -csv %s > %s' % (foldername, csvname))
            os.system(bashcmd) # Run

            # Filter/rename columns based on fields in config
            if self.fields is not None:
                # Load in csv as dataframe
                df = pd.read_csv(csvname, encoding = "ISO-8859-1",
                                 low_memory=False)
                headers = df.columns.to_list() # Grab headers
                # Fields of interest that exist in CSV:
                avail_fields_sh = [i for i in self.fields_short \
                                   if i in headers]
                # Longer name for those fields of interest
                avail_fields = [i for i in self.fields if \
                                i.split(':')[-1] in avail_fields_sh]
                # Grab only fields of interest in order
                df2 = df[avail_fields_sh]
                # Change names to long-form
                df2.columns = avail_fields
                # Save new
                df2.to_csv(csvname, index=False, encoding="ISO-8859-1")

            if self.verbose:
                print('Updated csv for %s' % sf)
        return


    def UpdateMetadata(self, subfolders=None):
        """
        For a given list of subfolders, loop through and update
        the metadata in the files of that folder to match the CSV
        using the exiftool update from csv command.

        **WARNING**: Dangerous function, directly modifies files
        in archive. Make sure to keep backups!

        Inputs:
            subfolders (list) : subfolders in which to update
                    files, default is all
        Outputs:
            Saves csv metadata into media files
        """

        # Check input
        if subfolders is None:
            subfolders = self.subfolders
        elif not isinstance(subfolders, list):
            subfolders = [subfolders]
        
        # Warn users to keep backups
        if self.verbose:
            print('Warning: Function directly modifies file metadata.\n'\
                   +'Make sure to keep a backup!')

        # Update metadata
        for sf in subfolders:
            # Grab absolute path of this subfolder
            foldername = os.path.join(self.CollectionPath, sf)

            # Recreate csv name from dir structure
            csvname = os.path.join(self.csvPath,
                                   sf.replace(os.sep,'__') + '.csv')

            # Run exiftool through bash shell command
            bashcmd = ('exiftool -csv=%s %s -overwrite_original_in_place -P -F'\
                       % (csvname, foldername))
            os.system(bashcmd) # Run

            if self.verbose:
                print('Updated metadata in %s' % sf)
        return


    def CreateBackup(self, subfolders=None, format='zip'):
        """
        Create a compressed backup of archive in secure folder
        Note: Function may fail for timestamps before 1980

        Inputs:
            subfolders (list) : subfolders to backup, default
                    is all, stored in containers one subdirectory
                    below CollectionPath
            format (str) : compression type to use with
                    shutil.make_archive(), e.g. 'zip', 'tar', 'gztar'
        Outputs:
            Saves a zip backup of the specified subfolders
        """
        import shutil
        if not os.path.exists(self.BackupPath):
            os.makedirs(self.BackupPath)

        # Check input
        if subfolders is None:
            subfolders = os.listdir(self.CollectionPath)
            # Grab only directories
            subfolders = [s for s in subfolders if \
                          os.path.isdir(os.path.join(self.CollectionPath,s))]
        elif not isinstance(subfolders, list):
            subfolders = [subfolders]

        # Zip folders
        for sf in subfolders:
            # Grab paths for this subfolder
            foldername = os.path.join(self.CollectionPath, sf)
            backupname = os.path.join(self.BackupPath,
                                      sf.replace(os.sep,'__'))
            # Compress files
            if self.verbose:
                print('Zipping ' + sf)
            shutil.make_archive(backupname, format, foldername)
        return


    def FindSource(self, searchterms, fields=None,
                   subfolders=None, include_all=False,
                   withPath=False):
        """
        For a given list of search terms, will return
        the filenames for files in which those terms appear
        in the specified metadata fields. Can choose which
        fields and folders in which to look.
        
        **NOTE** Intersection only works inside a single
        field, and does not behave well with wildcards. For
        reliable intersection, use multiple single-term
        searches with IntersectLists()

        Inputs:
            searchterms (list) : Terms for which to search.
                    Expects whole words!
            fields (list) : Metadata fields in which to look.
                    Shorthand expected. Default searches through
                    all in config.fields_short.
            subfolders (list) : Subfolders in which to search,
                    default is all
            include_all (bool) : Returns union of terms if False,
                    intersection if True. NOTE: Intersection only
                    works inside a single field. For comprehensive
                    intersection, use IntersectLists()
            withPath (bool) : Returns just filenames if False,
                    returns full path if true
        Outputs:
            FileNames (list) : List of file names containing terms
        """
        # Handle inputs
        if not isinstance(searchterms, list):
            searchterms = [searchterms]
        if fields is None:
            fields = self.fields_short
        if subfolders is None:
            subfolders = self.subfolders

        # Check if any searchterms either start or end in wildcards
        wildcard_border = False
        for term in searchterms:
            if (term[0] in '\/.*(),$^|?+') or (term[-1] in '\/.*(),$^|?+'):
                wildcard_border = True
        if wildcard_border and (len(searchterms) > 1):
            print('Multiple-term search does not work'\
                  + ' with wildcard-bordered terms')
            return []

        FileNames = []
        for sf in subfolders:
            # Recreate csv name from dir structure
            csvname = os.path.join(self.csvPath,
                                   sf.replace(os.sep,'__') + '.csv')
            # Read in csv
            df = pd.read_csv(csvname, encoding = "ISO-8859-1",
                             low_memory=False)

            # Loop through fields of interest:
            for jj in fields:
                # Find column name from shorthand
                xmp_col = [col for col in df.columns \
                           if jj == col.split(':')[-1]]
                # Skip if field not in csv
                if len(xmp_col) < 1:
                    continue
                else:
                    xmp_col = xmp_col[0]

                if len(searchterms) == 1:
                    # Check for special wildcards around edges of term
                    if wildcard_border:
                        # Create sub-df containing string,
                        # get sourcefile, make list
                        subdf = df[df[xmp_col].str.contains(searchterms[0],
                                                            regex=False, 
                                                            na=False)]
                        subdf = subdf['SourceFile'].values.tolist()
                    else:    
                        # If no wildcards, use regex to match whole words
                        term = r'\b%s\b' % re.escape(searchterms[0])
                        subdf = df[df[xmp_col].str.contains(term,
                                                            regex=True,
                                                            na=False)]
                        subdf = subdf['SourceFile'].values.tolist()
                    FileNames.extend(subdf)
                else:
                    # If multiple terms, use regex expression
                    # with either "and" or "or" operator
                    if include_all:
                        andterms = []
                        for term in searchterms:
                            andterms.append(r'(?=.*\b%s\b)' % re.escape(term))
                        subdf = df[df[xmp_col].str.contains(''.join(s for s in andterms),
                                                            na=False)]
                        subdf = subdf['SourceFile'].values.tolist()
                        FileNames.extend(subdf)
                    else:
                        term = ('|'.join(r'\b%s\b' % re.escape(s) for s in searchterms))
                        subdf = df[df[xmp_col].str.contains(term, na=False)]
                        subdf = subdf['SourceFile'].values.tolist()
                        FileNames.extend(subdf)

        # Remove duplicates if there are any
        FileNames = list(dict.fromkeys(FileNames))
        # Re-sort if necessary
        FileNames = sorted(FileNames)
        # If we don't want full path, grab just filenames
        if withPath is False:
            FileNames = [f.split(os.sep)[-1] for f in FileNames]
        return FileNames


    def GrabData(self, sourcefiles=None, fields=None,
                 startdate=None, enddate=None,
                 withPath=False):
        """
        Function will grab any metadata of interest for the
        specified list of files and return a pandas DataFrame.
        By default, returns all metadata in archive.
        
        Inputs:
            sourcefiles (list) : Files for which we want metadata.
                    Default is None, which will return everything.
            fields (list) : Metadata fields to return in DataFrame.
                    If None specified, returns default options.
            startdate (str) : Datetime (YYYYmmdd_HHMMSS) after which
                    to return data.
            enddate (str) : Datetime (YYYYmmdd_HHMMSS) before which
                    to return data.
            withPath (bool) : Returns just filenames in SourceFile
                    if False, returns full path if true
        Outputs:
            data (pandas DataFrame) : Dataframe of requested metadata.
        """
        # Load all metadata into dataframe
        frame = []
        for sf in self.subfolders:
            # Recreate csv name from dir structure
            csvname = os.path.join(self.csvPath,
                                   sf.replace(os.sep,'__') + '.csv')
            # Read in csv
            df = pd.read_csv(csvname, encoding = "ISO-8859-1",
                             low_memory=False)
            frame.append(df)
        df = pd.concat(frame)

        # Filter for the requested files, if specified
        if sourcefiles is not None:
            sourcefiles = '|'.join(map(re.escape, sourcefiles))
            df = df[df['SourceFile'].str.contains(sourcefiles)]

        # Make sure dates are recognizable as datetime
        df['CreateDate'] = pd.to_datetime(df['CreateDate'],
                                          format='%Y:%m:%d %H:%M:%S')
        # If filtering by date bounds:
        if startdate is not None:
            startdate = pd.to_datetime(startdate, format="%Y%m%d_%H%M%S")
            df = df[df['CreateDate'] >= startdate]
        if enddate is not None:
            enddate = pd.to_datetime(enddate, format="%Y%m%d_%H%M%S")
            df = df[df['CreateDate'] <= enddate]

        # Filter by requested fields
        if fields is None:
            fields = self.fields_short
        # Shorten column names to shorthand
        df.columns = [col.split(':')[-1] for col in df.columns]
        # Fields of interest that exist in CSV:
        avail_fields_sh = [i for i in fields \
                           if i in df.columns]
        # Grab only fields of interest in order
        df = df[avail_fields_sh]
        
        # Remove path from SourceFile if necessary
        if not withPath and ('SourceFile' in df.columns):
            SourceFiles = df['SourceFile'].tolist()
            SourceFiles = [s.split(os.sep)[-1] \
                           for s in SourceFiles]
            df['SourceFile'] = SourceFiles

        df.reset_index(drop=True, inplace=True)
        return df


    def CountUnique(self, series, delimiter=', '):
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