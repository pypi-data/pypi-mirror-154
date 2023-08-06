# -*- coding: utf-8 -*-
# =============================================================================>
# ##############################################################################
# ## 
# ## core.py
# ## 
# ##############################################################################
# =============================================================================>
# imports
try:
    from .tracker import *
    from .utils import *
    from .core import *
except Exception as _:
    from tracker import *
    from utils import *
    from core import *

import re
import discord

if __name__ == "__main__":

    with GGTrackerAPI(GAME.VALORANT) as gg:
        match_list = gg.get_match_result("Shiftなおった", "#4970", n_match = 1, mode = "unrated")
        
        match_list = convert_valorant_match_to_discord(match_list, min_out = False)
        # match_list = convert_valorant_match_to_ascii(match_list)
        # match_list = gg.get_pc_summary("Shiftなおった", "#4970", mode = "unrated")

        print(match_list[0])
    
