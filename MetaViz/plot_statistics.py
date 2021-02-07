#!/usr/bin/env python3
"""
Plotting routines dedicated to collection statistics
"""
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

#--------------------------------------
# Statistics Plots
#--------------------------------------
def HistogramYear(data, datefield='CreateDate', color='k'):
    """
    Plot a histogram of the CreateDate of files in data sorted by year
    
    Inputs:
        data (pandas.DataFrame) : DataFrame output of Archive.GrabData()
            containing the datefield specified
        datefield (str) : String name of the date field in data
        color (str) : Color of the bars of the histogram, must be
            recognizable to matplotlib.pyplot.hist()
    """
    year = data[datefield].dt.year.tolist()
    low = float(min(year))
    high = float(max(year))

    if len(plt.get_fignums()) < 1:
        fig, ax = plt.subplots(figsize=(5,2), dpi=200)
    else:
        ax = plt.gca()
    h = ax.hist(year, bins = int(high - low + 1),
                range = (low - 0.5, high + 0.5),
                density=True, rwidth=0.9, color='k')
    ax.set_xlim([low - 0.55, high + 0.55])
    b = plt.title('Yearly Statistics')
    return


def HistogramMonth(data, datefield='CreateDate', color='k'):
    """
    Plot a histogram of the CreateDate of files in data sorted by month
    
    Inputs:
        data (pandas.DataFrame) : DataFrame output of Archive.GrabData()
            containing the datefield specified
        datefield (str) : String name of the date field in data
        color (str) : Color of the bars of the histogram, must be
            recognizable to matplotlib.pyplot.hist()
    """
    mon = data[datefield].dt.month

    if len(plt.get_fignums()) < 1:
        fig, ax = plt.subplots(figsize=(5,2), dpi=200)
    else:
        ax = plt.gca()
    h = ax.hist(mon, bins=12, range=(0.5,12.5), 
                density=True, rwidth=0.9, color=color)
    ax.set_xlim([0.45, 12.55])
    ax.set_xticks(list(range(1, 13)))
    b = ax.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun',
                           'Jul','Aug','Sep','Oct','Nov','Dec'],
                           rotation=-40)
    b = plt.title('Monthly Statistics')
    return


def HistogramWeek(data, datefield='CreateDate', color='k'):
    """
    Plot a histogram of the CreateDate of files in data sorted
    by week of year
    
    Inputs:
        data (pandas.DataFrame) : DataFrame output of Archive.GrabData()
            containing the datefield specified
        datefield (str) : String name of the date field in data
        color (str) : Color of the bars of the histogram, must be
            recognizable to matplotlib.pyplot.hist()
    """
    week = data[datefield].dt.weekofyear

    if len(plt.get_fignums()) < 1:
        fig, ax = plt.subplots(figsize=(5,2), dpi=200)
    else:
        ax = plt.gca()
    h = ax.hist(week, bins=52, range=(0.5,52.5), 
                density=True, rwidth=0.9, color=color)
    ax.set_xlim([0.45, 52.55])
    ax.set_xticks(list(range(13, 53, 13)))
    b = plt.title('Weekly Statistics')
    return


def HistogramDay(data, datefield='CreateDate', color='k'):
    """
    Plot a histogram of the CreateDate of files in data sorted
    by day of year. Note: For leap years, days after leap day
    get collapsed onto their normal DOY, and Feb 29th gets
    assigned to Feb 28th
    
    Inputs:
        data (pandas.DataFrame) : DataFrame output of Archive.GrabData()
            containing the datefield specified
        datefield (str) : String name of the date field in data
        color (str) : Color of the bars of the histogram, must be
            recognizable to matplotlib.pyplot.hist()
    """
    day = data[datefield].dt.dayofyear.tolist()
    leaps = data[datefield].dt.is_leap_year.tolist()
    for ii in list(range(len(day))):
        if (leaps[ii]) & (day[ii] >= 60):
            day[ii] -= 1

    if len(plt.get_fignums()) < 1:
        fig, ax = plt.subplots(figsize=(5,2), dpi=200)
    else:
        ax = plt.gca()
    h = ax.hist(day, bins=365, range=(0.5,365.5), 
                density=True, rwidth=1, color=color)
    ax.set_xlim([0.45, 365.55])
    ax.set_xticks([31, 59, 90, 120, 151, 181,
                   212, 243, 273, 304, 334, 365])
    b = plt.title('Daily Statistics')
    return


def TemporalStats(data, datefield='CreateDate', color='k'):
    """
    Plot all temporal histograms together in a series of subplots.
    Includes year, then month, then week of year, then day of year.
    
    Inputs:
        data (pandas.DataFrame) : DataFrame output of Archive.GrabData()
            containing the datefield specified
        datefield (str) : String name of the date field in data
        color (str) : Color of the bars of the histogram, must be
            recognizable to matplotlib.pyplot.hist()
    """
    fig, (ax1,ax2,ax3,ax4) = plt.subplots(4,1,figsize=(5,8),dpi=300)
    # Year
    plt.sca(ax1)
    HistogramYear(data, datefield, color)
    ax1.set_title('Temporal Statistics Summary')
    ax1.set_xlabel('Year')
    # Month
    plt.sca(ax2)
    HistogramMonth(data, datefield, color)
    ax2.set_title(None)
    # Week
    plt.sca(ax3)
    HistogramWeek(data, datefield, color)
    ax3.set_title(None)
    ax3.set_xlabel('Week of Year')
    # Day
    plt.sca(ax4)
    HistogramDay(data, datefield, color)
    ax4.set_title(None)
    ax4.set_xlabel('Day of Year')
    plt.subplots_adjust(hspace=0.55)
    return