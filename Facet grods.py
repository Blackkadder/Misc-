# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 11:59:31 2016

@author: e115487
"""

import seaborn as sns
import pandas as pd 
import matplotlib.pyplot as plt

t_df=pd.read_csv('C:\\Users\\e115487\\Box Sync\\E175\\Data\\e175_data.csv')
t_df.head(2)
t_df['ASMs']

#style
sns.set_style("white")

#regplot
sns.lmplot(x='ASMs', y='Total Costs', data=t_df, hue='Al')
sns.lmplot(x='ASMs', y='Total Costs', data=t_df)


#facet grid
g = sns.FacetGrid(t_df, col="Al", hue="Al")
g.map(plt.scatter, "ASMs", "Total Costs", alpha=.7)
g.add_legend();

