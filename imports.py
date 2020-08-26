import os
from pathlib import Path
import re
import numpy as np
import xlrd
from matplotlib import pyplot as plt
import plotly.graph_objects as go
from tqdm import tqdm
import pandas as pd
import subprocess
import itertools
import shutil
import warnings
import glob
from pprint import pprint

from pymatgen.ext.matproj import MPRester, MPRestError
from pymatgen import Structure, Composition
from pymatgen.analysis.reaction_calculator import ComputedReaction
from pymatgen.entries.computed_entries import ComputedEntry, ComputedStructureEntry
from pymatgen.util.plotting import pretty_plot, periodic_table_heatmap
from pymatgen.core.periodic_table import Element
from pymatgen.io.vasp.outputs import Elfcar, Chgcar, Poscar, VolumetricData
from pymatgen.command_line.bader_caller import BaderAnalysis, bader_analysis_from_objects, index_mask_from_objects

from monty.serialization import loadfn, dumpfn
from monty.dev import requires
from monty.os.path import which
from monty.tempfile import ScratchDir
from monty.io import zopen

from pptx import Presentation
from pptx.util import Inches

from scipy.stats import linregress, skew, describe
from scipy.interpolate import RegularGridInterpolator
from sklearn.metrics import max_error, mean_absolute_error, mean_squared_error

print('Imports successfully loaded')


# def index_mask_from_objects2(chgcar, potcar=None, aeccar0=None, aeccar2=None):
#     """
#     Convenience method to retrieve an index mask Chgcar from running 
#     Bader analysis on a set of pymatgen Chgcar and Potcar objects.

#     This method will:

#     1. If aeccar objects are present, constructs a temporary reference
#     file as AECCAR0 + AECCAR2
#     2. Runs Bader analysis twice: once for charge, and a second time
#     for the charge difference (magnetization density).

#     :param chgcar: Chgcar object
#     :param potcar: (optional) Potcar object
#     :param aeccar0: (optional) Chgcar object from aeccar0 file
#     :param aeccar2: (optional) Chgcar object from aeccar2 file
#     :return: Chgcar containing index masks
#     """

#     with ScratchDir(".") as temp_dir:

#         if aeccar0 and aeccar2:
#             # construct reference file
#             chgref = aeccar0 + aeccar2
#             chgref_path = os.path.join(temp_dir, 'CHGCAR_ref')
#             try:
#                 chgref.write_file(chgref_path)
#             except ValueError:
#                 warnings.warn('Unable to  write CHGREF file. Won\'t be used in Bader analysis.')
#         else:
#             chgref_path = None

#         chgcar.write_file('CHGCAR')
#         chgcar_path = os.path.join(temp_dir, 'CHGCAR')

#         if potcar:
#             potcar.write_file('POTCAR')
#             potcar_path = os.path.join(temp_dir, 'POTCAR')
#         else:
#             potcar_path = None
            
# #         ba = BaderAnalysis(chgcar_path, potcar_filename=potcar_path, 
# #                            chgref_filename=chgref_path, atomic_partitions=True)
# #         return ba.index_mask
            
#         try:
#             ba = BaderAnalysis(chgcar_path, potcar_filename=potcar_path, 
#                                chgref_filename=chgref_path, atomic_partitions=True)
#             return ba.index_mask
#         except:
#             warnings.warn('Bader analysis failed. Returning None.')
    
# print('index_mask_from_objects2 succesfully loaded')

# def index_mask_from_objects4(chgcar, potcar=None, aeccar0=None, aeccar2=None):
#     """
#     Convenience method to retrieve an index mask Chgcar from running 
#     Bader analysis on a set of pymatgen Chgcar and Potcar objects.

#     This method will:

#     1. If aeccar objects are present, constructs a temporary reference
#     file as AECCAR0 + AECCAR2
#     2. Runs Bader analysis twice: once for charge, and a second time
#     for the charge difference (magnetization density).

#     :param chgcar: Chgcar object
#     :param potcar: (optional) Potcar object
#     :param aeccar0: (optional) Chgcar object from aeccar0 file
#     :param aeccar2: (optional) Chgcar object from aeccar2 file
#     :return: Chgcar containing index masks
#     """

#     with ScratchDir(".") as temp_dir:

#         if aeccar0 and aeccar2:
#             # construct reference file
#             chgref = aeccar0 + aeccar2
#             chgref_path = os.path.join(temp_dir, 'CHGCAR_ref')
#             try:
#                 chgref.write_file(chgref_path)
#             except ValueError as e:
#                 warnings.warn('Unable to  write CHGREF file. Won\'t be used in Bader analysis.')
#                 print(e)
#         else:
#             chgref_path = None

#         chgcar.write_file('CHGCAR')
#         chgcar_path = os.path.join(temp_dir, 'CHGCAR')

#         if potcar:
#             potcar.write_file('POTCAR')
#             potcar_path = os.path.join(temp_dir, 'POTCAR')
#         else:
#             potcar_path = None
            
#         ba = BaderAnalysis(chgcar_path, potcar_filename=potcar_path, 
#                            chgref_filename=chgref_path, atomic_partitions=True)
#         return ba.index_mask
    
# print('index_mask_from_objects4 succesfully loaded')