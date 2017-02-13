# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 14:02:56 2016

@author: e115487
"""


import plotly.plotly as py
from plotly.graph_objs import *

plotly.tools.set_credentials_file(username='Blackadder', api_key='e96hlqeh59')


trace0 = Scatter(
    x=[1, 2, 3, 4],
    y=[10, 15, 13, 17]
)
trace1 = Scatter(
    x=[1, 2, 3, 4],
    y=[16, 5, 11, 9]
)
data = Data([trace0, trace1])

py.iplot(data, filename = 'basic-line')