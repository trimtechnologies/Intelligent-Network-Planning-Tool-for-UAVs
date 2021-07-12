import quandl
import numpy as np
from sklearn import preprocessing, model_selection
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
import datetime

style.use('ggplot')

df = quandl.get("WIKI/GOOGL", api_key="m65eP3abS7_jRGAtVfFa")
df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Low']) / df['Adj. Close'] * 100.0
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0

df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]
forecast_col = 'Adj. Close'
df.fillna(value=-99999, inplace=True)
forecast_out = 1
df['label'] = df[forecast_col].shift(-forecast_out)

X = np.array(df.drop(['label'], 1))
X = preprocessing.scale(X)
X_lately = X[-forecast_out:]
X = X[:-forecast_out]

df.dropna(inplace=True)

y = np.array(df['label'])

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

# Instantiate regressors
reg_close = LinearRegression(n_jobs=-1)
reg_close.fit(X_train, y_train)

reg_hl = LinearRegression(n_jobs=-1)
reg_hl.fit(X_train, y_train)

reg_pct = LinearRegression(n_jobs=-1)
reg_pct.fit(X_train, y_train)

reg_vol = LinearRegression(n_jobs=-1)
reg_vol.fit(X_train, y_train)

# Prepare variables for loop
last_close = df['Adj. Close'][-1]
last_date = df.iloc[-1].name.timestamp()
df['Forecast'] = np.nan
predictions_arr = X_lately

for i in range(100):
    # Predict next point in time
    last_close_prediction = reg_close.predict(predictions_arr)
    last_hl_prediction = reg_hl.predict(predictions_arr)
    last_pct_prediction = reg_pct.predict(predictions_arr)
    last_vol_prediction = reg_vol.predict(predictions_arr)

    # Create np.Array of current predictions to serve as input for future predictions
    predictions_arr = np.array((last_close_prediction, last_hl_prediction, last_pct_prediction, last_vol_prediction)).T
    next_date = datetime.datetime.fromtimestamp(last_date)
    last_date += 86400

    # Outputs data into DataFrame to enable plotting
    df.loc[next_date] = [np.nan, np.nan, np.nan, np.nan, np.nan, float(last_close_prediction)]

df['Adj. Close'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()