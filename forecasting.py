import pandas as pd
from statsmodels.tsa.vector_ar.var_model import VAR
import numpy as np

# Load the dataset
data = pd.read_csv('assets/data/realistic_production_data.csv')

# Select the columns to use
columns_to_use = ['date', 'machine_id', 'cycle_time', 'downtime', 'production_count']
data = data[columns_to_use]

# Convert 'date' to datetime format
data['date'] = pd.to_datetime(data['date'])

# Sort data by date and machine_id
data = data.sort_values(by=['date', 'machine_id'])

# Initialize a DataFrame to store all forecasts
all_forecasts = []

# Group the data by 'machine_id' and apply the ARIMA forecast for each machine
grouped = data.groupby('machine_id')

for machine_id, group in grouped:
    # Sort the group by date
    group = group.sort_values(by='date')

    # Train a VAR model for multivariate forecasting
    model = VAR(group[['production_count', 'cycle_time', 'downtime']])
    model_fit = model.fit(maxlags=15)

    # Forecast the next 5 days (as there are 6 machines per day)
    forecast_steps = 30
    forecast = model_fit.forecast(y=group[['production_count', 'cycle_time', 'downtime']].values, steps=forecast_steps)

    # Create a new DataFrame for forecasted data
    forecast_dates = pd.date_range(start=group['date'].max() + pd.Timedelta(days=1), periods=forecast_steps, freq='D')
    forecast_df = pd.DataFrame(forecast, columns=['production_count', 'cycle_time', 'downtime'])
    forecast_df['date'] = forecast_dates
    forecast_df['machine_id'] = machine_id

    # Append the forecast_df to the list
    all_forecasts.append(forecast_df)

# Concatenate all forecasts into a single DataFrame
forecast_result = pd.concat(all_forecasts)

# Round values for better readability
forecast_result['cycle_time'] = forecast_result['cycle_time'].round(2)
forecast_result['downtime'] = forecast_result['downtime'].round(2)
forecast_result['production_count'] = forecast_result['production_count'].round(1)

# Rearrange columns to the correct order
forecast_result = forecast_result[['date', 'machine_id', 'cycle_time', 'downtime', 'production_count']]
# Sort the forecasted data by date and machine_id
forecast_result = forecast_result.sort_values(by=['date', 'machine_id'])

# Save the forecasted data to a new CSV file with the correct column order
forecast_result.to_csv('assets/result/forecasted_production_data_reordered.csv', index=False)
