# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 15:59:01 2016

@author: e115487
"""

#import
import pandas as pd
import seaborn as sns
#style
sns.set_style("white")
sns.set_context("notebook")

#data

file=pd.read_csv('C:\\Users\\e115487\\Box Sync\\2016 Revenue AOP\\gdp distribution.csv')

df=pd.DataFrame(file)

#density

    
dev = df['Deviation'].dropna()

sns.distplot(dev*100)
sns.distplot(df['WSJ_errors']*100)


sns.kdeplot(df['WSJ_errors']*100,bw=0.2)
sns.kdeplot(dev*100,bw=0.5)


    
