#!/usr/bin/env python3
"""
Plotting routines dedicated to magnitudes, i.e. the relative
prominence of different keywords in exif metadata fields
"""
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm


def BarChart(data, N=40, exclude=None, include=None):
    """
    Horizontal bar chart showing relative magnitudes
    of entries in the DataFrame "data", which contains
    the output of a call to Archive.CountUnique()
    
    Inputs:
        data (pandas DataFrame) : DataFrame output of
            Archive.CountUnique() which contains the values
            used for plotting
        N (int or bool) : Number of entries to show on the chart
        exclude (list or bool) : List of entries in data to
            specifically exclude from the plot
        include (list or bool) : List of entries in data to
            specifically include in the plot
    """
    x = data['Entry'].tolist()
    y = data['Count'].tolist()
    if N is None:
        N = len(data['Entry'])
    
    # Filter the data
    if exclude is not None:
        for exc in exclude:
            y = [y[i] for i in list(range(len(y))) if exc not in x[i]]
            x = [x[i] for i in list(range(len(x))) if exc not in x[i]]
    if include is not None:
        y = [y[i] for i in list(range(len(y))) if x[i] in include]
        x = [x[i] for i in list(range(len(x))) if x[i] in include]

    colors = cm.jet((np.log(y)-1) / float(np.log(max(y))))

    # Do plotting
    fig, ax = plt.subplots(1, 1, figsize=(4,N*7/30), dpi=150)
    mybar = ax.barh(x[0:N], y[0:N], log=True, alpha=0.7,
                    color=colors, edgecolor='k')
    ax.set_xlabel('Appearances')
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_title('Appearances')
    ax.set_axisbelow(True)
    ax.xaxis.grid(color='gray', which='both', alpha=0.3)
    yl = ax.set_ylim([N, -1])
    return


def PieChart(data, N=20, exclude=None, include=None):
    """
    Regular pie chart showing relative magnitudes
    of entries in the DataFrame "data", which contains
    the output of a call to Archive.CountUnique()
    
    Inputs:
        data (pandas DataFrame) : DataFrame output of
            Archive.CountUnique() which contains the values
            used for plotting
        N (int or bool) : Number of entries to show on the chart
        exclude (list or bool) : List of entries in data to
            specifically exclude from the plot
        include (list or bool) : List of entries in data to
            specifically include in the plot
    """
    x = data['Entry'].tolist()
    y = data['Count'].tolist()
    if N is None:
        N = len(data['Entry'])
    
    # Filter the data
    if exclude is not None:
        for exc in exclude:
            y = [y[i] for i in list(range(len(y))) if exc not in x[i]]
            x = [x[i] for i in list(range(len(x))) if exc not in x[i]]
    if include is not None:
        y = [y[i] for i in list(range(len(y))) if x[i] in include]
        x = [x[i] for i in list(range(len(x))) if x[i] in include]
    
    # Do plotting
    fig, ax = plt.subplots(1,1,figsize=(5,5), dpi=150)
    mypie = ax.pie(y, labels=x, startangle=45)
    for pie_wedge in mypie[0]:
        pie_wedge.set_edgecolor('white')
    ax.set_title('Appearances')
    ax.axis('equal')
    plt.show()
    return