import pandas as pd 
import numpy as np
import logging 


def time_of_day(hour):
    try:
        if 5 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 17:
            return "Afternoon"
        elif 17 <= hour < 21:
            return "Evening"
        else:
            return "Night"

    except Exception as e:
        logging.error(f"Time of day extraction failed due to: {e}")
        raise e 


def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Summer"
    elif month in [6, 7, 8, 9]:
        return "Monsoon"
    else:
        return "Post-Monsoon"
    

def date_time_features(df):
    try:
        logging.info("Starting date and time feature engineering...")

        df['Date'] = pd.to_datetime(df['Date'])
        df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')

        df['Month'] = df['Date'].dt.month
        df['Day'] = df['Date'].dt.day
        df['DayOfWeek'] = df['Date'].dt.day_name()
        df['Quarter'] = df['Date'].dt.quarter
        df['IsWeekend'] = (df['Date'].dt.dayofweek >= 5).astype(int)
        df['Hour'] = df['Time'].dt.hour
        df['TimeOfDay'] = df['Hour'].apply(time_of_day)
        df['Season'] = df['Month'].apply(get_season)

        df.drop(columns=['Date', 'Time'], inplace=True)

        logging.info("Date and time feature engineering completed.")

        return df

    except Exception as e:
        logging.error(f"Date-Time feature engineering failed due to: {e}")
        raise