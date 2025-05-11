import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.tools.tools import pinv_extended 
from patsy import dmatrices

import numpy as np
import pandas as pd
from pathlib import Path
import os.path
import os
import io
import math
import requests
import time 
import csv

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
print([matplotlib.__version__])
import seaborn as sns

DATA_PATH = Path.cwd()


fileSolar = './Hackathon/merged/collectedNorm.csv'
solarDF = pd.read_csv(fileSolar, delimiter=',')

print(solarDF.columns.values) 
print(solarDF)


formula = 'power_new ~ power_exist + nRel  + power_exist:nRel:kk_mio_rel + kk_mio_rel' 
'''
lm_all = smf.glm(formula=formula, data=solarDF, family=sm.families.Gaussian())
#lm_all_results = lm_all.fit()
lm_all_results = lm_all.fit_regularized(refit=True, zero_tol=0.002, L1_wt=0.7, maxiter=100)
'''

mod = smf.ols(formula=formula, data=solarDF)

res = mod.fit()


print(res.summary())

#print("ALL (Eval1, Eval2, Fit) \n")
#print(lm_all_results.summary())


