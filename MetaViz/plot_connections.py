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


def Heatmap1(Archive, field, N=20, exclude=None, include=None):
    """
    For the top N keywords in field, plot a heatmap showing the
    extent to which those keywords tend to appear along with
    other keywords inside the SAME metadata field.
    
    Differs from Heatmap2, which looks for connections BETWEEN fields.
    
    Inputs:
        Archive (obj) : archive.Archive() object used to access
            metadata fields via FindSource()
        field (str) : Field in which to look for keywords
        N (int) : Number of entries to show on the chart
        exclude (list or bool) : List of entries in data to
            specifically exclude from the plot
        include (list or bool) : List of entries in data to
            specifically include in the plot
    """
    # Get top entries in field
    data = Archive.GrabData(None, [field])
    data = tools.CountUnique(data[field], delimiter=', ')
    x = data['Entry'].tolist()

    # Filter the data
    if exclude is not None:
        for exc in exclude:
            x = [x[i] for i in list(range(len(x))) if exc not in x[i]]
    if include is not None:
        x = [x[i] for i in list(range(len(x))) if x[i] in include]
    keywords = x[0:N]

    # Initialize matrix of intersection counts
    matrix = np.zeros((len(keywords),len(keywords)), dtype=float)

    # Loop through and find intersection counts
    for ii, name_A in enumerate(keywords):
        for jj, name_B in enumerate(keywords):
            if jj > ii:
                A = Archive.FindSource([name_A], [field])
                B = Archive.FindSource([name_B], [field])
                AB = tools.IntersectLists([A, B])
                matrix[ii, jj] = len(AB)/(len(A)+len(B)-len(AB))

    # Make symmetric:
    matrix = (matrix + matrix.T - np.diag(np.diag(matrix))).tolist()

    # Do plotting
    fig = plt.figure(figsize=(6,6), dpi=200)
    plt.imshow(matrix, cmap='CMRmap')
    ax = plt.gca()
    ax.set_yticks(list(np.arange(0, N)))
    b = ax.set_yticklabels(keywords)
    ax.set_xticks(list(np.arange(0, N)))
    b = ax.set_xticklabels(keywords, rotation=-90)
    c = plt.colorbar(fraction=0.045)
    ax.set_title('Keyword Correlation in %s' % field)
    return