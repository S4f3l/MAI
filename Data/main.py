import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings

warnings.filterwarnings("ignore")

df = pd.read_csv('input.csv')
df['date'] = pd.to_datetime(df['date'])

predict_horizon = 18
last_date = df['date'].iloc[-1]
future_dates = pd.date_range(start=last_date + pd.offsets.MonthBegin(1),
                             periods=predict_horizon, freq='MS')

output_df = pd.DataFrame({'date': future_dates})

for column in df.columns:
    if column != 'date':
        series = pd.to_numeric(df[column], errors='coerce').fillna(df[column].mean())
        model = SARIMAX(series,
                        order=(1, 1, 1),
                        seasonal_order=(1, 0, 1, 12),
                        enforce_stationarity=False,
                        enforce_invertibility=False)

        model_fit = model.fit(disp=False)
        forecast = model_fit.forecast(steps=predict_horizon)

        output_df[column] = forecast.values

final_df = pd.concat([df, output_df], ignore_index=True)

final_df.to_csv('output.csv', index=False)
print("Файл output.csv успешно создан")