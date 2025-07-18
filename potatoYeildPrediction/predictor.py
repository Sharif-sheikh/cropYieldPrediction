import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy.interpolate import lagrange
import numpy as np

# Load and filter dataset
df = pd.read_csv("FAOSTAT_data_en_5-30-2025.csv")
potatoes_df = df[df['Item'] == 'Potatoes'].sort_values('Year')

# Get available years and values
years = potatoes_df['Year'].tolist()
values = potatoes_df['Value'].tolist()

# Detect missing years between min and max
full_years = list(range(min(years), max(years) + 1))
missing_years = sorted(set(full_years) - set(years))

# Lagrange interpolation to fill missing values
if missing_years:
    interpolation_model = lagrange(years, values)
    interpolated_rows = []

    for year in missing_years:
        interpolated_value = interpolation_model(year)
        interpolated_rows.append({'Year': year, 'Value': interpolated_value, 'Item': 'Potatoes'})

    # Add interpolated rows to original DataFrame
    potatoes_df = pd.concat([potatoes_df, pd.DataFrame(interpolated_rows)], ignore_index=True)
    potatoes_df = potatoes_df.sort_values('Year')

# Prepare data for linear regression
X = potatoes_df[['Year']]
y = potatoes_df[['Value']]
model = LinearRegression()
model.fit(X, y)

# Single year prediction
def predict_crop(year: int) -> float:
    pred = model.predict([[year]])
    return round(pred[0][0], 2)

# Range prediction
def predict_crop_range(start_year: int, end_year: int):
    results = []
    for year in range(start_year, end_year + 1):
        pred = model.predict([[year]])
        results.append((year, round(pred[0][0], 2)))
    return results
