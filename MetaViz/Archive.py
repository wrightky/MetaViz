#!/usr/bin/env python3
"""
Establish main class for the photo archive/collection
"""
import numpy as np
import os
import pandas
import subprocess
import re
import .config as cf

class Archive():
    """Parent class for the media collection"""
    def __init__(self):
        # Store details on collection location
        self.CollectionPath = cf.CollectionPath
        self.csvPath = cf.csvPath
        self.subfolders = cf.subfolders
        
        # Information on packages
        self.SeabornAvailable = cf.SeabornAvailable
        self.ChordAvailable = cf.ChordAvailable
        self.NetworkXAvailable = cf.NetworkXAvailable
