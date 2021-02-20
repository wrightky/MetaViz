#!/usr/bin/env python3
"""
Configuration file to establish global features of the archive.
Includes things like primary directories and package settings.
"""
import os

#---------------------------------------------------------
# Input information on your archive
#---------------------------------------------------------
# Absolute path to the media collection
CollectionPath = r'/Users/mickeylanning/Pictures/AllMediaArchive'

# List of any folders inside collection to exclude from processing
ExcludeFolders = ['Images']

# Absolute path of location to save CSV files
csvPath = r'/Users/mickeylanning/Pictures/Metadata'

# Absolute path of location to create backup zip archive
BackupPath = r'/Users/mickeylanning/Pictures/Backup'

# Metadata fields of interest, list or None
# Decides the order and header of columns in CSVs
fields = ['SourceFile',
          'XMP-dc:Title',
          'XMP-dc:Description',
          'XMP-dc:Coverage',
          'XMP-dc:Subject',
          'CreateDate',
          'XMP-dc:Creator',
          'FileModifyDate',
          'XMP-digiKam:ImageHistory',
          'XMP-acdsee:Notes',
          'XMP-dc:Source',
          'Duration']

# Set global verbose flag for printed function outputs
verbose = True

#---------------------------------------------------------
# Grabbing additional information
#---------------------------------------------------------
if fields is not None:
    # Shorthand for metadata fields
    fields_short = [f.split(':')[-1] for f in fields]

# Create CSV path if it doesn't exist yet
if not os.path.exists(csvPath):
    os.makedirs(csvPath)

# Grab all sub-directory names, excluding any specified above
subfolders = [x[0] for x in os.walk(CollectionPath)]
for ex_fold in ExcludeFolders:
    subfolders = [s for s in subfolders if ex_fold not in s]
subfolders = [s.replace(CollectionPath,'')[1:] for s in subfolders[1:]]

#---------------------------------------------------------
# Check for auxilary packages
#---------------------------------------------------------
try:
    import seaborn
    SeabornAvailable = True
except ImportError:
    SeabornAvailable = False

try:
    from chord import Chord
    ChordAvailable = True
except ImportError:
    ChordAvailable = False

try:
    import networkx
    NetworkXAvailable = True
except ImportError:
    NetworkXAvailable = False

try:
    import cv2
    OpenCVAvailable = True
except ImportError:
    OpenCVAvailable = False

try:
    from PIL import Image
    PillowAvailable = True
except ImportError:
    PillowAvailable = False

try:
    import plotly
    PlotlyAvailable = True
except ImportError:
    PlotlyAvailable = False

try:
    import geopy
    GeoPyAvailable = True
except ImportError:
    GeoPyAvailable = False