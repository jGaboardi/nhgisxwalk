__version__ = "0.1.2"
"""
# `nhgisxwalk` --- IPUMS/NHGIS Census Crosswalk and Atom Generator

# This file is part of the Minnesota Population Center's NHGISXWALK.
# For copyright and licensing information, see the NOTICE and LICENSE files
# in this project's top-level directory, and also on-line at:
#   https://github.com/ipums/nhgisxwalk

"""

__author__ = "James Gaboardi <jgaboardi@gmail.com>"
__date__ = "2020-04"


from .geocrosswalk import GeoCrossWalk
from .geocrosswalk import calculate_atoms, round_weights, str_types
from .geocrosswalk import valid_geo_shorthand, example_crosswalk_data
from .geocrosswalk import prepare_data_product, generate_data_product
from .geocrosswalk import xwalk_df_to_csv, xwalk_df_from_csv
from .geocrosswalk import extract_state, extract_unique_stfips
from .geocrosswalk import regenerate_blk_blk_xwalk, split_xwalk
from .geocrosswalk import SORT_PARAMS, SORT_BYS
from .geocrosswalk import ID_COLS, CSV, ZIP, TXT

from .variable_codes import code_desc_1990, desc_code_1990
from .variable_codes import code_desc_2000_SF1b, desc_code_2000_SF1b
from .variable_codes import code_desc_2000_SF3b, desc_code_2000_SF3b
