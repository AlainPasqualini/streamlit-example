from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

st.title('Interactive ‘what if’ analysis: electricity consumers going off-grid with renewables + batteries')
"""

The continuous cost reduction in renewables now makes them profitable enough to compete with other assets, without subsidies (when focusing on LCOE calculation, a methodology taking into account both capital and O&M expenses). However, to truly go off-grid, a consumer needs not only to generate power with renewables, but also match generation and consumption.

Electrochemical batteries can complete a renewables asset to reach balance between generation and load. Yet, they remain an expensive, and less profitable, investment. However, the constant increase in T&D (Transport and Distribution) and consumption taxes, now reaching about 70% of the complete electricity price (link), might change the game faster than we think.

For this article, I wanted to experiment with interactive python code (and deployment/hosting of this code). I hope you might enjoy tweaking the parameters of this ‘what if’ analysis.


"""
st.header('Input parameters:')

data_DE=pd.read_csv('DE.csv')

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
st.markdown('•	_battery round-trip efficiency: 92% (source: Lazard, for Li-ion)_')
•	the consumer relies on its battery for 50% of its total energy consumption
example: an consumer previously consuming 10MWh each day from the grid will need to invest enough to get 5MWh each day from battery discharge, and to generate (5+5/0.92)=10.43 of electricity (note that the calculation takes into account the 0.92 from battery efficiency)
•	security of supply factor: 140%. Example: The 10.43MWh/day of solar energy required in the previous example are increased to 14.6, to take into account interday and interseason variability of renewables power generation
•	electricity from the grid, at wholesale price, is valued at 40€/MWh for 2021 and beyond
"""

#st.image('./header.png')



