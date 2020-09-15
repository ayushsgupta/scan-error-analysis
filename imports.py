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

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

from scipy.stats import linregress, skew, describe
from scipy.interpolate import RegularGridInterpolator
from sklearn.metrics import max_error, mean_absolute_error, mean_squared_error, average_precision_score, \
                            explained_variance_score, mean_squared_log_error
from sklearn.linear_model import LinearRegression, SGDRegressor, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import cross_val_score, GridSearchCV

from pint import UnitRegistry
ureg = UnitRegistry()
AVOGADRO = 6.02214076e23 # https://en.wikipedia.org/wiki/Avogadro_constant
KJMOLtoEV = 0.01036410 # http://wild.life.nctu.edu.tw/class/common/energy-unit-conv-table.html
ureg.define('atom = 1/{} mol'.format(AVOGADRO))
Quantity = ureg.Quantity

def sample(d, thresh=0.05):
    for k in d.keys():
        if np.random.random_sample() < thresh:
            print(k, ':', d[k])

print('Imports successfully loaded')


# def experimental_formation_energy(f):
#     janaf_series = janaf_data.loc[janaf_data.Formula==f]
#     flipped = flip_formula(f)
#     janaf_series_f = janaf_data.loc[janaf_data.Formula==flipped]
#     if not janaf_series.empty:
#         target = None
#         for phase in janaf_phase_preferences:
#             target = janaf_series.loc[janaf_data.Phase==phase]
#             if not target.empty:
#                 break
# #         if len(target['DeltaH_298'].values) > 1:
# #             print(f, target, '\n--------------------------------\n')
#         formation_energy = target['DeltaH_298'].values[0] / 1000 * KJMOLtoEV
#     elif not janaf_series_f.empty:
#         target = None
#         for phase in janaf_phase_preferences:
#             target = janaf_series_f.loc[janaf_data.Phase==phase]
#             if not target.empty:
#                 break
#         if len(target['DeltaH_298'].values) > 1:
#             print(f, target, '\n--------------------------------\n')
#         formation_energy = target['DeltaH_298'].values[0] / 1000 * KJMOLtoEV
#     else:
#         formation_energy = mp_expt_data[f]
#     return formation_energy
