#!/usr/bin/env python3
"""
Plotting routines dedicated to time-series or temporal trends
"""
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm

#--------------------------------------
# Time-Series Plots
#--------------------------------------
def OccurancePlot(archive,
                  searchterms,
                  fields=None,
                  alpha=0.2,
                  startdate=None,
                  enddate=None):
    """
    Plots a time-series of occurances of a given
    set of search terms in the collection as a scatter
    plot of vertical lines
    
    Inputs:
        archive (obj) : MetaViz.Archive object
        searchterms (list) : Terms for which to search.
        fields (list) : Metadata fields in which to look.
                Shorthand expected. Default searches through
                all in config.fields_short.
        alpha (float) : Alpha of marker face
        startdate (str) : Datetime (YYYYmmdd_HHMMSS) after which
                to return data.
        enddate (str) : Datetime (YYYYmmdd_HHMMSS) before which
                to return data.
    """
    # Instantiate figure
    plt.figure(figsize=(8,len(searchterms)*1.3/3), dpi=200)
    # Handle colors (tab10 or brg)
    colors = cm.tab10(np.arange(len(searchterms)) \
                      / float(len(searchterms)))
    np.random.shuffle(colors)

    for ii, term in enumerate(searchterms):
        # Find filenames with search terms in field
        sourcefiles = archive.FindSource([term], fields)
        # Grab and filter by datetimes 
        data = archive.GrabData(sourcefiles, ['CreateDate'],
                                startdate=startdate,
                                enddate=enddate)
        # Plot scatterplot w/ default spacing settings
        plt.scatter(data['CreateDate'],
                    np.ones(len(data['CreateDate']))*(len(searchterms)-ii),
                    s=400, color=colors[ii], marker='|', alpha=alpha)
    plt.ylim([0.5, len(searchterms) + 0.5])
    plt.yticks(list(range(len(searchterms),0,-1)), searchterms)
    plt.title('Occurances by Date')
    return


def OccuranceMagnitude(archive,
                       searchterms,
                       fields=None,
                       alpha=0.4,
                       scale=5,
                       startdate=None,
                       enddate=None):
    """
    Plots a scatterplot time-series of occurances of
    a given set of search terms in the collection,
    with sizes of each marker reflecting the number
    of appearances that day
    
    Inputs:
        archive (obj) : MetaViz.Archive object
        searchterms (list) : Terms for which to search.
        fields (list) : Metadata fields in which to look.
                Shorthand expected. Default searches through
                all in config.fields_short.
        alpha (float) : Alpha of marker face
        scale (int) : Scaling factor to apply to all markers
        startdate (str) : Datetime (YYYYmmdd_HHMMSS) after which
                to return data.
        enddate (str) : Datetime (YYYYmmdd_HHMMSS) before which
                to return data.
    """
    # Instantiate figure
    plt.figure(figsize=(8,len(searchterms)*1.3/3), dpi=300)
    # Get array of colors from hsv:
    colors = cm.hsv(np.arange(len(searchterms)) \
                    / float(len(searchterms)))
    colors = np.array(colors)
    colors[:,3] = alpha
    np.random.shuffle(colors)

    for ii, term in enumerate(searchterms):
        # Find filenames with search terms in field
        sourcefiles = archive.FindSource([term], fields)
        # Grab and filter by datetimes 
        data = archive.GrabData(sourcefiles, ['CreateDate'],
                                startdate=startdate,
                                enddate=enddate)
        # Count totals by day
        counts = data['CreateDate'].dt.normalize().value_counts()
        dates = counts.index.to_series()
        # Plot scatterplot w/ default spacing settings
        plt.scatter(dates, np.ones(len(dates))*(len(searchterms)-ii),
                    s=counts*scale, color=colors[ii], marker='o',
                    edgecolors=(0,0,0,1), linewidth=0.5)
    plt.ylim([0.5, len(searchterms) + 0.5])
    plt.yticks(list(range(len(searchterms),0,-1)), searchterms)
    plt.title('Occurances by Date')
    return