#!/usr/bin/env python3
"""
Plotting routines dedicated to connections, i.e. the
association of keywords with other keywords in the
exif metadata fields
"""
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
from . import config as cf
from . import tools

#--------------------------------------
# Connections Plots
#--------------------------------------
def ChordChart(Archive, keywords, fields):
    """
    Plots a chord chart showing the degree to which the specified
    keywords appear together in the given metadata fields. Thickness
    of the chords corresponds to the strength of the connection,
    and is fully interactive.
    
    NOTE: Requires auxilary "chord" module, and only works in Jupyter
    lab (not notebook)
    
    Inputs:
        Archive (obj) : archive.Archive() object used to access
            metadata fields via FindSource()
        keywords (list) : List of keyword arguments used for each
            chord, specified as strings. Argument used as the
            'searchterms' argument in FindSource()
        fields (list) : List of fields in which to look for keywords,
            used as 'fields' argument in FindSource()
    """
    # Check if Chord is available
    if not cf.ChordAvailable:
        print("Function unavailable, requires installation of Chord")
        print("See installation guide for auxilary packages")
        return
    from chord import Chord
    
    # Initialize matrix of intersection counts
    matrix = np.zeros((len(keywords),len(keywords)))

    # Loop through and find intersection counts
    for ii, name_A in enumerate(keywords):
        for jj, name_B in enumerate(keywords):
            if jj > ii:
                A = Archive.FindSource([name_A], fields)
                B = Archive.FindSource([name_B], fields)
                matrix[ii, jj] = len(tools.IntersectLists([A, B]))

    # Make symmetric:
    matrix = (matrix + matrix.T - np.diag(np.diag(matrix))).tolist()

    # Plot
    Chord(matrix, keywords, width=600).show()
    return