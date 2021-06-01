from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

st.title('Interactive ‘what if’ analysis: electricity consumers going off-grid with renewables + batteries')
"""

The continuous cost reduction in renewables now makes them profitable enough to compete with other assets, without subsidies (when focusing on LCOE calculation, a methodology taking into account both capital and O&M expenses). However, to truly go off-grid, a consumer needs not only to generate power with renewables, but also match generation and consumption.

Electrochemical batteries can complete a renewables asset to reach balance between generation and demand. Yet, they remain an expensive, and less profitable, investment. However, the constant increase in T&D (Transport and Distribution) and consumption taxes, now reaching about 70% of the complete electricity price (in the EU), might change the game faster than we think.

For this article, I wanted to experiment with interactive python code (and deployment/hosting of this code). I hope you might enjoy tweaking the parameters of this ‘what if’ analysis.


"""
st.header('Input parameters:')

geo=st.selectbox('Select a geography', ['France','Germany','Spain'])

TD_fare_escalation = st.slider("Set T&D fares escalation for 2021 and beyond (%/year):", -5, 15, 4)
"""
for comparison, most EU countries went throught about a 4% escalation over 2010-2020 (source: Eurostat)
"""
solar_evolution = st.slider("Set PV price evolution for 2021 and beyond (%/year):", -25, 5, -11)
"""
for comparison, utility-scale solar LCOE went throught a CAGR of -11% over 2010-2020 (source: Lazard publications)
"""
battery_evolution = st.slider("Set batteries price evolution for 2021 and beyond (%/year):", -25, 5, -4)
"""
for comparison, commercial and Industrial batteries (coupled with PV) went throught a CAGR of -4% over 2018-2020 (source: Lazard publications)
"""
st.header('Other hypothesis:')
"""
•	battery round-trip efficiency: 92% (source: Lazard, for Li-ion)
"""
"""
•	the consumer relies on its battery for 50% of its total energy consumption.
_Example: a consumer previously consuming 10MWh each day from the grid will need to invest enough to get 5MWh each day from battery discharge, and to generate (5+5/0.92)=10.43MWh of electricity (note that the calculation takes into account the 0.92 from battery efficiency)_
"""
"""
•	security of supply factor: 140%. _Example: The 10.43MWh/day of solar energy required in the previous example are increased to 14.6MWh/day, to take into account interday and interseason variability of renewables power generation._
"""
"""
•	electricity from the grid, at wholesale price, is valued at 40€/MWh for 2021 and beyond_


In order to keep things simple, I approximated the categories of energy consumers and their behavior when facing this binary choice:
•	remain on the grid, and keep paying ever-increasing T&D fares and electricity bill
"""
"""
•	or, invest in PV+battery system, then go off-grid
"""
"""
Both choices are compared in terms of cost per MWh of consumed electricity for the next 10 years. Energy intensive industries (such as glass, for which energy represents more than 30% of the total cost) might be early adopters: going off-grid as soon as a slight economy is possible. Meanwhile, other industries take longer to be convinced. Here is a chart to illustrate my hypotheses:
#st.image('./header.png')

The model will also take into account that the more consumers leave, the less consumers remain to finance the grid; therefore, forcing T&D operators to increase the fares to break even. This will come on top of natural T&D price escalation, and leads to a positive feedback loop inciting more consumer leave the grid.
"""
st.header('Outputs:')
"""
And finally, the output of the what-if analysis:
"""
data_GE=pd.read_csv('GE.csv',index_col=0)
data_FR=pd.read_csv('FR.csv',index_col=0)
data_SP=pd.read_csv('SP.csv',index_col=0)
data_LCOS=pd.read_csv('LCOS.csv',index_col=0)
data=pd.read_csv('article2.csv',index_col=0)

def leaving_large(x):
  out=max(0,min(-x/0.2,1))
  return out

def leaving_medium(x):
  out=0.5*max(0,min((-x+0.2)/0.2,1))
  return out

def leaving_resid(x):
  out=0.1*max(0,min((-x+0.4)/0.2,1))
  return out
#when LCOE ready, load it here into data

if geo=='Germany':
  data_geo=data_GE
else:
  if geo=='Spain':
    data_geo=data_SP
  else:
    data_geo=data_FR

for y in list([2018,2019,2020]):
  #make cols off-grid when data ready
  data.loc[y,'TD_large']=data_geo.loc[y,'large IC']-0.04
  data.loc[y,'TD_medium']=data_geo.loc[y,'medium IC']-0.04
  data.loc[y,'TD_resid']=data_geo.loc[y,'residential']-0.04
  data.loc[y,'sum_TD']=data.loc[y,'TD_large']+data.loc[y,'TD_medium']+data.loc[y,'TD_resid']
  data.loc[y,'left_large']=0
  data.loc[y,'left_medium']=0
  data.loc[y,'left_resid']=0
  data.loc[y,'SUM_TD_after_left']=data.loc[y,'TD_large']*(1-data.loc[y,'left_large'])+data.loc[y,'TD_medium']*(1-data.loc[y,'left_medium'])+data.loc[y,'TD_resid']*(1-data.loc[y,'left_resid'])
  data.loc[y,'adjust_coeff']=data.loc[y,'sum_TD']/data.loc[y,'SUM_TD_after_left']
  data.loc[y,'grid energy cost (large consumer, excl. VAT)']=0.04+data.loc[y,'adjust_coeff']*data.loc[y,'TD_large']
  data.loc[y,'grid energy cost (medium consumer, excl. VAT)']=0.04+data.loc[y,'adjust_coeff']*data.loc[y,'TD_medium']
  data.loc[y,'grid energy cost (residential consumer, incl. VAT)']=0.04+data.loc[y,'adjust_coeff']*data.loc[y,'TD_resid']
  
for y in range(2021,2036):
  #make cols off-grid when data ready
  data.loc[y,'TD_large']=data.loc[y-1,'TD_large']*(1+TD_fare_escalation/100)
  data.loc[y,'TD_medium']=data.loc[y-1,'TD_medium']*(1+TD_fare_escalation/100)
  data.loc[y,'TD_resid']=data.loc[y-1,'TD_resid']*(1+TD_fare_escalation/100)
  data.loc[y,'sum_TD']=data.loc[y,'TD_large']+data.loc[y,'TD_medium']+data.loc[y,'TD_resid']
  #update this code when LCOE and LCOS ready
  data.loc[y,'left_large']=0
  data.loc[y,'left_medium']=0
  data.loc[y,'left_resid']=0
  data.loc[y,'SUM_TD_after_left']=data.loc[y,'TD_large']*(1-data.loc[y,'left_large'])+data.loc[y,'TD_medium']*(1-data.loc[y,'left_medium'])+data.loc[y,'TD_resid']*(1-data.loc[y,'left_resid'])
  data.loc[y,'adjust_coeff']=data.loc[y,'sum_TD']/data.loc[y,'SUM_TD_after_left']
  data.loc[y,'grid energy cost (large consumer, excl. VAT)']=0.04+data.loc[y,'adjust_coeff']*data.loc[y,'TD_large']
  data.loc[y,'grid energy cost (medium consumer, excl. VAT)']=0.04+data.loc[y,'adjust_coeff']*data.loc[y,'TD_medium']
  data.loc[y,'grid energy cost (residential consumer, incl. VAT)']=0.04+data.loc[y,'adjust_coeff']*data.loc[y,'TD_resid']
  
  
st.write(data)
