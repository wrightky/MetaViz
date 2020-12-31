#!/usr/bin/env python3
"""
Establish main class for the photo archive/collection
"""
import numpy as np
import pandas as pd
import os
import subprocess
import re
from . import config as cf

class Archive():
    """Parent class for the media collection"""
    def __init__(self):
        # Store details on collection location
        self.CollectionPath = cf.CollectionPath
        self.csvPath = cf.csvPath
        self.subfolders = cf.subfolders
        self.fields = cf.fields
        self.fields_short = cf.fields_short
        
        # Information on packages
        self.SeabornAvailable = cf.SeabornAvailable
        self.ChordAvailable = cf.ChordAvailable
        self.NetworkXAvailable = cf.NetworkXAvailable
    
    def UpdateCSV(self, subfolders=None):
        """For a given list of subfolders, loop through and update the
        exiftool csv for that year. Must be called before later functions
        in this script.

        Inputs:
            subfolders (list) : subfolders to update, default is all
        Outputs:
            outputs (list) : outputs from the subprocess exiftool call
            Saves new csv files for specified folders in csvPath"""

        # Check input
        if subfolders is None:
            subfolders = self.subfolders
        elif not isinstance(subfolders, list):
            subfolders = [subfolders]

        outputs = []
        for sf in subfolders:
            # Grab absolute path of this subfolder
            foldername = os.path.join(self.CollectionPath, sf)

            # Create a name for csv preserving dir structure
            if os.sep in sf:
                csvname = sf.replace(os.sep,'__')
            csvname = os.path.join(self.csvPath, csvname + '.csv')

            # Run exiftool through bash shell command
            bashcmd = ('exiftool -csv %s > %s' % (foldername, csvname))
            output = subprocess.check_output(bashcmd, shell=True) # Run
            outputs.append(output)

            # Filter/rename columns based on fields in config
            if self.fields is not None:
                # Load in csv as dataframe
                df = pd.read_csv(csvname, encoding = "ISO-8859-1")
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

            print('Updated csv for %s' % sf)
        return outputs
