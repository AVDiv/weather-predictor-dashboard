from datetime import datetime, timedelta
import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_option_menu import option_menu
import numpy as np

# with st.sidebar:
selected = option_menu(
  menu_title=None,
  options=["Rainfall", "Insights"],
  menu_icon='cast',
  icons=["cloud-rain", "graph-up-arrow"],
  orientation="horizontal",
  default_index=0,
)



weather_df = pd.read_csv('./data/forecasted_temp.csv')
# weather_df['time'] = pd.to_datetime(weather_df['time'], format='%Y-%m-%d %H:%M:%S')
weather_df = weather_df.astype({'time': 'datetime64[ns]'})


def rainfall_panel():
  st.title('Sri Lanka rainfall prediction')
  date_filter = st.date_input('Date', value=datetime(2021, 1, 1))
  date_yesterday = date_filter - timedelta(days=1)
  weather_emoji = {
    '': '',
    0: ':sunny:',
    1: ':mostly_sunny:',
    2: ':partly_sunny:',
    3: ':partly_sunny:',
    51: ':umbrella_with_rain_drops:',
    53: ':umbrella_with_rain_drops:',
    55: ':umbrella_with_rain_drops:',
    61: ':rain_cloud:',
    63: ':rain_cloud:',
    65: ':rain_cloud:' 
  }
  filtered_weather_df = weather_df[pd.to_datetime(weather_df['time']) == pd.to_datetime(date_filter)]
  print(filtered_weather_df)
  city_list = filtered_weather_df['city'].unique()
  city_columns = []
  
  if len(city_list) == 0:
    st.write('No data available for the selected date.')
    return
  
  for _ in range(len(city_list)):
    st.write('')
    st.write('')
    city_columns.extend(st.columns(3))

  for city_item_index in range(len(city_list)):
    city_data = None
    try:
      city_data = filtered_weather_df[filtered_weather_df['city'] == city_list[city_item_index]].iloc[0]
      city_rainfall = city_data['rain_sum']
      city_weather_code = city_data['weathercode']
      city_temperature = city_data['apparent_temperature_mean']
      city_rainfall_delta = city_rainfall - weather_df[(weather_df['city'] == city_list[city_item_index]) & (weather_df['time'] == date_yesterday.strftime('%Y-%m-%d'))]['rain_sum'].iloc[0]
      city_rainfall = f'{city_rainfall :.2f} mm'
      city_rainfall_delta = f"{city_rainfall_delta: .2f} mm"
      try:
        weather_code = weather_emoji[city_weather_code]
        city_columns[city_item_index].metric(f'##### {weather_emoji[city_weather_code]} {city_list[city_item_index]} - {city_temperature} °C', city_rainfall, city_rainfall_delta)
      except Exception as e:
        city_columns[city_item_index].metric(f'##### {city_list[city_item_index]} - {city_temperature :.2f} °C', city_rainfall, city_rainfall_delta)
    except Exception as e:
      city_data = None
      print(e)


def insights_panel():
  st.title('Insights')
  date_cols = st.columns(2)
  start_date_filter = date_cols[0].date_input('Start date', value=datetime(2021, 1, 1))
  end_date_filter = date_cols[1].date_input('End date', value=datetime(2021, 12, 31))
  city_select = st.multiselect('Select city', weather_df['city'].unique().tolist(), default=weather_df['city'].unique().tolist())
  filtered_weather_df = weather_df[weather_df['city'].isin(city_select)]
  filtered_weather_df['time'] = pd.to_datetime(filtered_weather_df['time'])
  filtered_weather_df = filtered_weather_df[(filtered_weather_df['time'].dt.date >= start_date_filter) & (filtered_weather_df['time'].dt.date <= end_date_filter)]
  st.write('#### Rainfall by city (mm)')
  chart = px.line(filtered_weather_df, x='time', y='rain_sum', color='city', title=None, template='plotly_dark')
  st.plotly_chart(chart)
  st.write('#### Average temperature by city (°C)')
  chart = px.line(filtered_weather_df, x='time', y='apparent_temperature_mean', color='city', title=None, template='plotly_dark')
  st.plotly_chart(chart)

if selected == 'Rainfall':
  rainfall_panel()
elif selected == 'Insights':
  insights_panel()