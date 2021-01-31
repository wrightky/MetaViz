__version__ = "0.1.0"

# Interfacing with the metadata
from . import config
from .archive import Archive
Archive = Archive()

# Plotting routines
from .plot_timeseries import *
from .plot_magnitudes import *
from .plot_connections import *

# Other tools and functions
from .tools import *
from . import tools_datenames as dnt