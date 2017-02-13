# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 15:51:49 2017

@author: e115487
"""

## panda panda panda
import pandas as pd
import datetime as dt
from pandasql import sqldf
import numpy as np

## read data
diio_data1 = pd.read_csv('G:/RevNetworkAnalysis/Economic & Industry Analysis/Projects/OA Capacity/Data/20170117_diio raw/Schedule_Dynamic_Table_Report_119188.tsv',skiprows=3,skipfooter=16,sep='\t')

diio_data2 = pd.read_csv('G:/RevNetworkAnalysis/Economic & Industry Analysis/Projects/OA Capacity/Data/20170117_diio raw/Schedule_Dynamic_Table_Report_119187.tsv',skiprows=3,skipfooter=16,sep='\t')

diio_data3 = pd.read_csv('G:/RevNetworkAnalysis/Economic & Industry Analysis/Projects/OA Capacity/Data/20170117_diio raw/Schedule_Dynamic_Table_Report_119186.tsv',skiprows=3,skipfooter=16,sep='\t')

diio_data2.head()

diio_data2.tail()

diio_data = pd.concat([diio_data1,diio_data2,diio_data3])

diio_data.reset_index()

diio_data.to_csv('G:/RevNetworkAnalysis/Economic & Industry Analysis/Projects/OA Capacity/Data/20160116_data.csv')