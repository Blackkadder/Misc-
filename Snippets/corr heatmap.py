# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 15:51:27 2016

@author: e115487
"""
#import
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import statsmodels.api as sm
import seaborn as sns
#style
sns.set_style("white")
sns.set_context("notebook")

#data

file=pd.read_csv('C:\\Users\\e115487\\Box Sync\\2016 Revenue AOP\\explore.csv')

df=pd.DataFrame(file)


#create datetime
rng = pd.date_range('1/1/1993', '10/1/2017', freq='QS')
df=df.set_index(rng)


#create training set
train=df['1/1/1994':'10/1/2015']
# Compute the correlation matrix
corr = train.corr()

# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True


# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(15, 12))
# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, 
            square=True, 
            linewidths=.5, cbar_kws={"shrink": .6},ax=ax)
            
            
            