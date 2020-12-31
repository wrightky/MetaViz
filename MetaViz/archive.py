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
                print('Updated photos in %s' % sf)
        return


    def CreateBackup(self, subfolders=None, format='zip'):
        """
        Create a compressed backup of archive in secure folder
        Note: Function may fail for timestamps before 1980

        Inputs:
            subfolders (list) : subfolders to backup, default
                                is all, stored in containers one
                                subdirectory below CollectionPath
            format (str) : compression type to use with
                           shutil.make_archive(), e.g. 'zip',
                           'tar', 'gztar'
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