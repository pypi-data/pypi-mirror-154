# -*- coding: utf-8 -*-
# =============================================================================>
# ##############################################################################
# ## 
# ## __init__.py
# ## 
# ##############################################################################
# =============================================================================>
# imports default

# =============================================================================>
# imports third party

# =============================================================================>
# imports local

try:
    from . import tracker
    from . import utils
    from .core import *
except Exception as _:
    import tracker
    import utils
    from core import *

__copyright__ = "Copyright (C) 2022 nakashimas and ggpython authors"
__version__ = "0.0.0"
__license__ = "MIT"
__author__ = "nakashimas"
__author_email__ = "nascor.neco@gmail.com"
__url__ = "https://github.com/nakashimas/ggpython"
