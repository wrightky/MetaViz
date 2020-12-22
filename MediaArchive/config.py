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
CollectionPath = r'/Pictures/AllPhotos_GroupedByDate'

# Absolute path of location to save CSV files
csvPath = r'/Pictures/Metadata'

# List of any folders inside collection to exclude from processing
ExcludeFolders = ['Images']

#---------------------------------------------------------
# Grabbing additional information
#---------------------------------------------------------
# Create CSV path if it doesn't exist yet
if not os.path.exists(csvPath):
    os.makedirs(csvPath)

# Grab all sub-directory names, excluding any specified above
subfolders = [f.path for f in os.scandir(CollectionPath) if f.is_dir()]
for ex_fold in ExludeFolders:
    subfolders = [s for s in subfolders if ex_fold not in s]

# Check which tertiary plotting packages are available
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
