#!/usr/bin/env python3
"""
Plotting routines dedicated to time-series or temporal trends
"""
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
from . import config as cf

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


def ViolinPlot(archive, terms, fields,
               refdate='19800101_000000',
               palette='Set2', inner='points',
               scale='area', cut=0, linewidth=0.8):
    """
    Wrapper for the Seaborn violin plot function. For each keyword
    in terms, find files for which that keyword appears in fields,
    and plot a violin of occurances by date. Most other attributes
    are aesthetic adjustments fed into seaborn.violinplots()
    
    Inputs:
        archive (obj) : MetaViz.Archive object
        terms (list) : Keywords to search for in Archive, fed into
            Archive.FindSource()
        fields (list) : Exif fields in which to search for terms,
            fed into Archive.FindSource()
        refdate (str) : Reference date which is used to convert
            pandas datetime to numeric dates, ideally a value
            similar to the dates returned from the collection
        palette, inner, scale, cut, linewidth : See requirements
            for seaborn.violinplot()
    """
    # Check if Seaborn is available
    if not cf.SeabornAvailable:
        print("Function unavailable, requires installation of Seaborn")
        print("See installation guide for auxilary packages")
        return
    import seaborn as sns
    sns.set_theme(style="whitegrid")

    dates = []
    refdate = pd.to_datetime(refdate, format="%Y%m%d_%H%M%S")
    for n, term in enumerate(terms):
        # Create a random dataset across several variables
        sourcefiles = archive.FindSource([term], fields)
        # Grab and filter by datetimes 
        data = archive.GrabData(sourcefiles, ['CreateDate'])
        # Convert to numeric date
        data['epoch'] = (data['CreateDate']-refdate)//pd.Timedelta("1d")
        # Save to list
        dates.append(data['epoch']/365.0 + refdate.year)

    # Append all the dates into a new dataframe
    df = pd.concat(dates, axis=1, keys=terms)

    # Show each distribution with both violins and points
    fig, ax = plt.subplots(figsize=(3,len(terms)/1.5), dpi=200)
    ax = sns.violinplot(data=df, ax=ax, width=0.95, orient='h',
                        palette=palette, inner=inner, scale=scale,
                        cut=cut, linewidth=linewidth)
    return


def RidgePlot(archive, terms, fields,
              refdate='19800101_000000',
              palette='deep', bw_adjust=0.5,
              aspect=8, height=0.8):
    """
    Wrapper for the Seaborn Ridge plot. For each keyword
    in terms, find files for which that keyword appears in fields,
    and plot a kernel of occurances by date. Most other attributes
    are aesthetic adjustments fed into seaborn, see example at
    https://seaborn.pydata.org/examples/kde_ridgeplot.html
    
    Inputs:
        archive (obj) : MetaViz.Archive object
        terms (list) : Keywords to search for in Archive, fed into
            Archive.FindSource()
        fields (list) : Exif fields in which to search for terms,
            fed into Archive.FindSource()
        refdate (str) : Reference date which is used to convert
            pandas datetime to numeric dates, ideally a value
            similar to the dates returned from the collection
        palette (str) : Seaborn color palette
        bw_adjust (float) : Smoothness of the kernel
        aspect (float) : width/height of figure
        height (float) : height of each FacetGrid
    """
    # Check if Seaborn is available
    if not cf.SeabornAvailable:
        print("Function unavailable, requires installation of Seaborn")
        print("See installation guide for auxilary packages")
        return
    import seaborn as sns
    sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

    dates = []
    refdate = pd.to_datetime(refdate, format="%Y%m%d_%H%M%S")
    for n, term in enumerate(terms):
        # Create a random dataset across several variables
        sourcefiles = archive.FindSource([term], fields)
        # Grab and filter by datetimes 
        data = archive.GrabData(sourcefiles, ['CreateDate'])
        dfl = pd.DataFrame()
        # Convert to numeric date
        dfl['epoch'] = (data['CreateDate']-refdate)//pd.Timedelta("1d")
        dfl['epoch'] = dfl['epoch']/365.0 + refdate.year
        # Create term column to create long-form tidy df
        dfl['term'] = np.tile(term, len(dfl['epoch']))
        dates.append(dfl)
    # Append all the dates into a new dataframe
    df = pd.concat(dates)

    # Initialize the FacetGrid object
    g = sns.FacetGrid(df, row="term", hue="term",
                      aspect=aspect, height=height, palette=palette)

    # Draw the densities in a few steps
    g.map(sns.kdeplot, "epoch",
          bw_adjust=bw_adjust, clip_on=False,
          fill=True, alpha=1, linewidth=1.5)
    g.map(sns.kdeplot, "epoch", clip_on=False, 
          color="w", lw=2, bw_adjust=bw_adjust)
    g.map(plt.axhline, y=0, lw=2, clip_on=False)

    # Define and use a simple function to label the plot in axes coordinates
    def label(x, color, label):
        ax = plt.gca()
        ax.text(0, .2, label, fontweight="bold", color=color,
                ha="left", va="center", transform=ax.transAxes, fontsize=14)
    g.map(label, "epoch")

    # Set the subplots to overlap
    g.fig.subplots_adjust(hspace=-0.25)

    # Other minor details for tuning the plot
    g.set_titles("")
    g.set(yticks=[])
    g.despine(bottom=True, left=True)
    ax = plt.gca()
    ax.tick_params(axis='x', which='major', labelsize=10, color='k')
    ax.set_xlabel(None)
    plt.gcf().set_dpi(200)
    return