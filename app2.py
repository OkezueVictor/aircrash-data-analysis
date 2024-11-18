import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np


def load_data():
    file = 'aircrahesFullDataUpdated_2024.csv'
    df= pd.read_csv(file)
    df.rename(columns={'Aircraft Manufacturer':'Manufacturer',
                'Country/Region':'Country',
                'Fatalities (air)':'Fatalities'}, 
                inplace=True)
    df = df.sort_values(by='Year', ascending=True)
    df.reset_index(drop=True, inplace=True)
    df.Aircraft = df.Aircraft.str.replace("?","")
    return df
# load the data set
df = load_data()

# Total Deaths Analysis
df['Total_deaths'] = df['Fatalities'] + df['Ground']
Total_deaths=df['Total_deaths']
# Calculating Number of survivors
df['Survivor'] = df['Aboard'] - df['Fatalities']
No_of_Survivors = df['Survivor']
# Fatality rate Analysis
df['Fatality Rate'] = df['Fatalities'] / df['Aboard']
Fatality_Rate = df['Fatality Rate']


# Title of our app
st.title('AIR CRASHES ANALYSIS')

# Removing comma from the 'Year' column
df['Year'] = df['Year'].astype(str)
df['Year'] = df['Year'].str.replace(',',' ')

# Calculations and matrices
year = df['Year'].unique()
selected_year = st.sidebar.multiselect(
                    "Choose The Year",
                    year,
                    [year[15],
                    year [20],
                    year[25],
                    year[56]
                    ])
filtered_table = df[df['Year'].isin(selected_year)]


# Total Fatality
if len (filtered_table) > 0:
    Total_fatalities = filtered_table['Fatalities'].sum()
else:
    Total_fatalities = df.Fatalities.sum()  

# Total deaths
if len (filtered_table) > 0:
    Total_deaths = filtered_table['Total_deaths'].sum()
else:
    Total_deaths = df['Total_deaths'].sum()

# Fatality Rate
if len (filtered_table) > 0:
    Fatality_Rate = filtered_table['Fatality Rate'].count()
else:
    Fatality_Rate = df['Fatality Rate'].count()

# Survivor Analysis
if len (filtered_table) > 0:
    No_of_Survivors = filtered_table['Survivor'].sum()
else:
    No_of_Survivors = df['Survivor'].sum()

# Display of metrics
st.subheader("Summary")
col1, col2, col3 = st.columns([0.5,0.5,0.5], gap="small")
col1.metric(
    label = "Total Deaths",
    value = f"{Total_deaths:,}")
col2.metric(
    label = "Fatality Rate",
    value = f"{Fatality_Rate:,}")
col3.metric(
    label = "No. of Survivors",
    value = f"{No_of_Survivors:,}")
# end of metrics

# Display specific columns in dataframe
st.dataframe(filtered_table [["Year","Month","Country","Aircraft","Fatalities","Ground",
                      "Aboard","Total_deaths","Fatality Rate"]], width = 700, height = 300)

# Crash analysis per year
Crash_per_year = filtered_table.groupby('Year').size().sort_values(ascending=True)
try:
    st.write("# Crashes per year")
    st.bar_chart(Crash_per_year,
                 color="#ffaa00")
    xlabel = "Year"
    ylabel = "No of crashes"
except ValueError as e:
    st.error(
        """ Error: """ % e.reason
    )

# Crash Analysis per month
Crash_per_month = filtered_table.groupby('Month').size().sort_values(ascending=True)
try:
    st.write("# Crashes per month")
    st.bar_chart(Crash_per_month,
                 color="#ffaa00")
    xlabel = "Month"
    ylabel = "No of crashes"
except ValueError as e:
    st.error(
        """ Error: """ % e.reason
    )

# Analysis for Total Fatalities in Air crash
Fatalities_per_year = filtered_table.groupby('Year')['Fatalities'].sum().sort_values(ascending=True)
try:
    st.write("# Total Fatalities in Air crashes per year")
    st.bar_chart(Fatalities_per_year,
                 color="#ffaa0088")
    xlabel = "Year"
    ylabel = "No of Fatalities"
except ValueError as e:
    st.error(
        """ Error: """ % e.reason
    )

# Analysis for top 10 aircraft involved in crashes
Crash_by_aircraft = df['Aircraft'].value_counts().head(10).sort_values(ascending=True)
try:
    st.write("# Top 10 Aircraft involved in crashes")
    st.bar_chart(Crash_by_aircraft,
                 color="#ffaa0088")
    xlabel = "No of Crashes"
    ylabel = "Aircraft Type"
except ValueError as e:
    st.error(
        """ Error: """ % e.reason
    )

# Analysis for top 10 countries invoved in crashes
Crash_by_country = df['Country'].value_counts().head(10)
try:
    st.write("# Top 10 countries involved in crashes")
    st.bar_chart(Crash_by_country,
                 color="#ffaa0088")
    xlabel = "Number of crashes"
    ylabel = "Country"
except ValueError as e:
    st.error(
        """ Error: """ % e.reason
    )

# Bar chart for Total No. of operators
Operators = df['Operator'].value_counts().head(10)
try:
    st.write("# Total number of operators")
    st.bar_chart(Operators,
                 color="#ffaa00")
    xlabel = "Fatality Rate"
    ylabel = "Frequency"
except ValueError as e:
    st.error(
        """ Error: """ % e.reason
    )

st.button('Rerun')