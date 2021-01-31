__version__ = "0.0.1"

# Interfacing with the metadata
from . import config
from .archive import Archive
Archive = Archive()

# Plotting routines
from .plot_timeseries import *
from .plot_magnitude import *

# Other tools and functions
from .tools import *
from . import tools_datenames as dnt