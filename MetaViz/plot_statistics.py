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


def HeatmapMonth(data, datefield='CreateDate',
                 uselog=True, cmap='magma'):
    """
    Plot a 2D heatmap of the number of files in data sorted by
    year on the x-axis and month on the y-axis. Color axis
    defaults to log scale to show relative structure.
    
    Inputs:
        data (pandas.DataFrame) : DataFrame output of Archive.GrabData()
            containing the datefield specified
        datefield (str) : String name of the date field in data
        uselog (bool) : Flag decides whether to show color axis in
            linear or log10 space
        cmap (str) : Matplotlib colormap to be used for the heatmap
    """
    # Isolate important date information 
    years = data[datefield].dt.year.to_numpy()
    months = data[datefield].dt.month.to_numpy()

    yr_mon_sorted = np.zeros((12, (max(years)+1-min(years))), dtype=float)
    # Loop through years
    for yy in np.arange(min(years), max(years)+1, 1):
        months_this_year = months[years==yy]
        # Loop through months
        for mm in (np.arange(12)+1):
            yr_mon_sorted[mm-1, yy-min(years)] = \
                np.count_nonzero(months_this_year==mm)

    if uselog:
        yr_mon_sorted[yr_mon_sorted==0] = 0.5
        yr_mon_sorted = np.log10(yr_mon_sorted)

    # Create figure
    fig = plt.figure(figsize=(5,5), dpi=200)
    plt.imshow(yr_mon_sorted, cmap=cmap,
               extent=[min(years), max(years)+1, 12.5, 0.5])
    ax = plt.gca()
    ax.set_aspect((max(years)+1-min(years))/20)
    ti = plt.title('Media Files by Month')

    cbar = plt.colorbar(fraction=0.0277)
    if uselog:
        cticks = [c for c in cbar.ax.get_yticks() if c.is_integer()]
        fig.delaxes(cbar.ax)
        cbar = plt.colorbar(fraction=0.0277, ticks=cticks)
        cbar.ax.set_yticklabels([str(int(10.**c)) for c in cticks])

    ax.set_yticks(list(range(1, 13)))
    b = ax.set_yticklabels(['Jan','Feb','Mar','Apr','May','Jun',
                           'Jul','Aug','Sep','Oct','Nov','Dec'])
    ticks = ax.get_xticks()
    ticks = [t for t in ticks if t <= max(years) and t >= min(years)]
    b = ax.set_xticks([int(x) for x in ticks if x.is_integer()])
    return


def HeatmapWeek(data, datefield='CreateDate',
                uselog=True, cmap='gnuplot2'):
    """
    Plot a 2D heatmap of the number of files in data sorted by
    year on the x-axis and week of year on the y-axis. Color axis
    defaults to log scale to show relative structure.
    
    Inputs:
        data (pandas.DataFrame) : DataFrame output of Archive.GrabData()
            containing the datefield specified
        datefield (str) : String name of the date field in data
        uselog (bool) : Flag decides whether to show color axis in
            linear or log10 space
        cmap (str) : Matplotlib colormap to be used for the heatmap
    """
    # Isolate important date information
    years = data[datefield].dt.year.to_numpy()
    weeks = data[datefield].dt.weekofyear.to_numpy()

    yr_week_sorted = np.zeros((52, (max(years)+1-min(years))), dtype=float)
    # Loop through years
    for yy in np.arange(min(years), max(years)+1, 1):
        weeks_this_year = weeks[years==yy]
        # Loop through weeks
        for ww in (np.arange(52)+1):
            yr_week_sorted[ww-1, yy-min(years)] = \
                np.count_nonzero(weeks_this_year==ww)

    if uselog:
        yr_week_sorted[yr_week_sorted==0] = 0.5
        yr_week_sorted = np.log10(yr_week_sorted)

    # Create figure
    fig = plt.figure(figsize=(5,5), dpi=200)
    plt.imshow(yr_week_sorted, cmap=cmap,
               extent=[min(years), max(years)+1, 52.5, 0.5])
    ax = plt.gca()
    ax.set_aspect((max(years)+1-min(years))/86.7)
    ti = plt.title('Media Files by Week of Year')

    cbar = plt.colorbar(fraction=0.0277)
    if uselog:
        cticks = [c for c in cbar.ax.get_yticks() if c.is_integer()]
        fig.delaxes(cbar.ax)
        cbar = plt.colorbar(fraction=0.0277, ticks=cticks)
        cbar.ax.set_yticklabels([str(int(10.**c)) for c in cticks])

    ax.set_yticks(list(np.arange(1, 52, 4.33)))
    ax.set_yticklabels(['Jan','Feb','Mar','Apr','May','Jun',
                        'Jul','Aug','Sep','Oct','Nov','Dec'])
    ticks = ax.get_xticks()
    ticks = [t for t in ticks if t <= max(years) and t >= min(years)]
    b = ax.set_xticks([int(x) for x in ticks if x.is_integer()])
    return


def HeatmapDay(data, datefield='CreateDate',
               uselog=True, cmap='inferno'):
    """
    Plot a 2D heatmap of the number of files in data sorted by
    year on the x-axis and day of year on the y-axis. Color axis
    defaults to log scale to show relative structure.
    
    Note: For leap years, days after leap day get collapsed onto 
    their normal DOY, and Feb 29th gets assigned to Feb 28th
    
    Inputs:
        data (pandas.DataFrame) : DataFrame output of Archive.GrabData()
            containing the datefield specified
        datefield (str) : String name of the date field in data
        uselog (bool) : Flag decides whether to show color axis in
            linear or log10 space
        cmap (str) : Matplotlib colormap to be used for the heatmap
    """
    # Isolate important date information, correct leaps
    years = data[datefield].dt.year.to_numpy()
    days = data[datefield].dt.dayofyear.to_numpy()
    leaps = data[datefield].dt.is_leap_year.tolist()
    for ii in list(range(len(days))):
        if (leaps[ii]) & (days[ii] >= 60):
            days[ii] -= 1

    yr_day_sorted = np.zeros((365, (max(years)+1-min(years))), dtype=float)
    # Loop through years
    for yy in np.arange(min(years), max(years)+1, 1):
        days_this_year = days[years==yy]
        # Loop through days
        for dd in (np.arange(365)+1):
            yr_day_sorted[dd-1, yy-min(years)] = \
                np.count_nonzero(days_this_year==dd)

    if uselog:
        yr_day_sorted[yr_day_sorted==0] = 0.5
        yr_day_sorted = np.log10(yr_day_sorted)

    # Create figure
    fig = plt.figure(figsize=(5,5), dpi=700)
    plt.imshow(yr_day_sorted, cmap=cmap,
               extent=[min(years), max(years)+1, 365.5, 0.5])
    ax = plt.gca()
    ax.set_aspect((max(years)+1-min(years))/608)
    ti = plt.title('Media Files by Day of Year')

    cbar = plt.colorbar(fraction=0.0277)
    if uselog:
        cticks = [c for c in cbar.ax.get_yticks() if c.is_integer()]
        fig.delaxes(cbar.ax)
        cbar = plt.colorbar(fraction=0.0277, ticks=cticks)
        cbar.ax.set_yticklabels([str(int(10.**c)) for c in cticks])

    ax.set_yticks([1, 32, 60, 91, 121, 152, 182,
                   213, 244, 274, 305, 335])
    ax.set_yticklabels(['Jan','Feb','Mar','Apr','May','Jun',
                        'Jul','Aug','Sep','Oct','Nov','Dec'])
    ticks = ax.get_xticks()
    ticks = [t for t in ticks if t <= max(years) and t >= min(years)]
    b = ax.set_xticks([int(x) for x in ticks if x.is_integer()])
    return