# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 16:58:26 2016

@author: e115487
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 17:59:01 2016

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

#plot_stuff def
def plot_stuff(model_name):
    print(model_name.summary())
    output_df= pd.DataFrame(train['Rev_SWA_adj'])
    output_df['Forecast'] = np.exp(model_name.predict())
    output_df['MAPE'] = np.absolute(output_df['Forecast']/output_df['Rev_SWA_adj']-1)
    output_df.loc[:,['MAPE']].plot()
    output_df.loc[:,['Rev_SWA_adj','Forecast']].plot()
    print('THIS IS THE MAPE ---------->>> ',np.mean(output_df['MAPE']))
    return   

#define model and run model
reg_gdp = smf.ols(formula='np.log(Rev_SWA) ~ np.log(GDP)+C(Period) ',data=train).fit()
reg_gdp_ind = smf.ols(formula='np.log(Rev_Ind) ~ np.log(GDP)+C(Period) ',data=train).fit()

reg_capacity = smf.ols(formula='np.log(Rev_SWA_adj) ~ np.log(GDP)*np.log(ASM_SWA_adj)',data=train).fit()
plot_stuff(reg_capacity)




reg_capacity = smf.ols(formula='np.log(Rev_SWA) ~  np.log(ASM_SWA_adj)+np.log(GDP)+C(Qtr) ',data=train).fit()
plot_stuff(reg_capacity)


#results
print(reg_gdp_ind.summary())
print('Parameters: ', regr2.params)
print('Standard errors: ', regr2.bse)
print('Predicted values: ', regr2.predict())




sns.lmplot(x='GDP',y='Rev_SWA',data=train,truncate=True,ci=False,fit_reg=True,col='Period',hue='Period',col_wrap=3,size=3,aspect=1.5,legend = False,scatter_kws={"s": 40})
plt.legend(loc='upper left')


sns.lmplot(x='GDP',y='Rev_SWA',data=train,truncate=True,ci=False,fit_reg=True,hue='Period',size=6,aspect=1.5,legend = False,scatter_kws={"s": 40})
plt.legend(loc='upper left')
#Industry

sns.lmplot(x='ASM_Ind',y='Rev_Ind',data=train,order=3,truncate=True,fit_reg=True,hue=None,size=6,aspect=2,legend = False,scatter_kws={"s": 70})
plt.legend(loc='upper left')


#SWA
sns.lmplot(x='ASM_SWA',y='Rev_SWA',data=train,order=3,fit_reg=True,hue=None,size=6,aspect=2,legend = False,scatter_kws={"s": 70})
plt.legend(loc='upper left')

#Dist
sns.distplot(train['YoY_ASM_SWA'])
sns.distplot(train['GDP_growth_real'])

np.std(train['GDP_growth_real'])
np.mean(train['GDP_growth_real'])
