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
        A = Archive.FindSource([name_A], fields)
        for jj, name_B in enumerate(keywords):
            if jj > ii:
                B = Archive.FindSource([name_B], fields)
                matrix[ii, jj] = len(tools.IntersectLists([A, B]))

    # Make symmetric:
    matrix = (matrix + matrix.T - np.diag(np.diag(matrix))).tolist()

    # Plot
    Chord(matrix, keywords, width=600).show()
    return


def Heatmap1(Archive, field, N=20, cmap='CMRmap',
             exclude=None, include=None):
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
        cmap (str) : Matplotlib colormap to be used for the heatmap
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
        A = Archive.FindSource([name_A], [field])
        for jj, name_B in enumerate(keywords):
            if jj > ii:
                B = Archive.FindSource([name_B], [field])
                AB = tools.IntersectLists([A, B])
                matrix[ii, jj] = len(AB)/(len(A)+len(B)-len(AB))

    # Make symmetric:
    matrix = (matrix + matrix.T - np.diag(np.diag(matrix))).tolist()

    # Do plotting
    fig = plt.figure(figsize=(0.4*N, 0.4*N), dpi=300)
    plt.imshow(matrix, cmap=cmap)
    ax = plt.gca()
    ax.set_yticks(list(np.arange(0, N)))
    b = ax.set_yticklabels(keywords)
    ax.set_xticks(list(np.arange(0, N)))
    b = ax.set_xticklabels(keywords, rotation=-90)
    c = plt.colorbar(fraction=0.045)
    ax.set_title('Keyword Correlation in %s' % field)
    return


def Heatmap2(Archive, field_x, field_y, 
             N_x=20, N_y=20, cmap='CMRmap',
             exclude_x=None, exclude_y=None, 
             include_x=None, include_y=None):
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
        cmap (str) : Matplotlib colormap to be used for the heatmap
        exclude (list or bool) : List of entries in data to
            specifically exclude from the plot
        include (list or bool) : List of entries in data to
            specifically include in the plot
    """
    # Get top entries in each field
    data = Archive.GrabData(None, [field_x])
    data = tools.CountUnique(data[field_x], delimiter=', ')
    x = data['Entry'].tolist()
    data = Archive.GrabData(None, [field_y])
    data = tools.CountUnique(data[field_y], delimiter=', ')
    y = data['Entry'].tolist()

    # Filter the data
    if exclude_x is not None:
        for exc in exclude_x:
            x = [x[i] for i in list(range(len(x))) if exc not in x[i]]
    if include_x is not None:
        x = [x[i] for i in list(range(len(x))) if x[i] in include_x]
    keywords_x = x[0:N_x]
    if exclude_y is not None:
        for exc in exclude_y:
            y = [y[i] for i in list(range(len(y))) if exc not in y[i]]
    if include_y is not None:
        y = [y[i] for i in list(range(len(y))) if y[i] in include_y]
    keywords_y = y[0:N_y]

    # Initialize matrix of intersection counts
    matrix = np.zeros((len(keywords_x),len(keywords_y)), dtype=float)

    # Loop through and find intersection counts
    for ii, name_A in enumerate(keywords_x):
        A = Archive.FindSource([name_A], [field_x])
        for jj, name_B in enumerate(keywords_y):
            B = Archive.FindSource([name_B], [field_y])
            AB = tools.IntersectLists([A, B])
            matrix[ii, jj] = len(AB)/(len(A)+len(B)-len(AB))

    # Do plotting
    fig = plt.figure(figsize=(0.4*N_x, 0.4*N_y), dpi=300)
    plt.imshow(matrix.T, cmap=cmap)
    ax = plt.gca()
    ax.set_yticks(list(np.arange(0, N_y)))
    b = ax.set_yticklabels(keywords_y)
    ax.set_xticks(list(np.arange(0, N_x)))
    b = ax.set_xticklabels(keywords_x, rotation=-90)
    c = plt.colorbar(fraction=0.045)
    ax.set_title('Keyword Correlation (%s and %s)' % (field_x, field_y))
    return