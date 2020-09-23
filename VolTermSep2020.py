import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

plt.rcParams['date.epoch'] = '000-12-31'
import seaborn as sns

sns.set()
from sklearn.preprocessing import RobustScaler
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.linear_model import Ridge
from sklearn.linear_model import RidgeCV
from statsmodels.api import Logit
from scipy.stats import spearmanr
import xlsxwriter
from pandas.plotting import register_matplotlib_converters
from sklearn.model_selection import train_test_split
from sklearn.model_selection import LeaveOneOut
from matplotlib import dates as mdates
from sklearn.decomposition import PCA
import plotly.graph_objects as go

# To fix the date fuck-ups
old_epoch = '0000-12-31T00:00:00'
new_epoch = '1970-01-01T00:00:00'
mdates.set_epoch(old_epoch)
register_matplotlib_converters()

os.chdir('/Users/anusarfarooqui/Docs/Matlab/')
# Clock utility function
import time


def TicTocGenerator():
    ti = 0
    tf = time.time()
    while True:
        ti = tf
        tf = time.time()
        yield tf - ti


TicToc = TicTocGenerator()


def toc(tempBool=True):
    tempTimeInterval = next(TicToc)
    if tempBool:
        print("Elapsed time: %f seconds.\n" % tempTimeInterval)


def tic():
    toc(False)
# %% Download VIX futures data
StrList = ["2021-03-17", "2021-04-21", "2021-05-19",
           "2021-02-17", "2021-01-20", "2020-01-22", "2020-02-19", "2020-03-18", "2020-04-15", "2020-05-20",
           "2020-06-17", "2020-07-22", "2020-08-19", "2020-09-16", "2020-10-21", "2020-11-18", "2020-01-08",
           "2020-01-15", "2020-01-29", "2020-02-05", "2020-02-12", "2020-02-26", "2020-03-04", "2020-03-10",
           "2020-03-25", "2020-04-01", "2020-04-08", "2020-04-22", "2020-04-29", "2019-01-16", "2019-02-13",
           "2019-03-19", "2019-04-17", "2019-05-22", "2019-06-19", "2019-07-17", "2019-08-21", "2019-09-18",
           "2019-10-16", "2019-11-20", "2019-12-18", "2019-01-02", "2019-01-09", "2019-01-23", "2019-01-30",
           "2019-02-06", "2019-02-20", "2019-02-27", "2019-03-06", "2019-03-13", "2019-03-27", "2019-04-03",
           "2019-04-10", "2019-04-24", "2019-05-01", "2019-05-08", "2019-05-15", "2019-05-29", "2019-06-05",
           "2019-06-12", "2019-06-26", "2019-07-03", "2019-07-10", "2019-07-24", "2019-07-31", "2019-08-07",
           "2019-08-14", "2019-08-28", "2019-09-04", "2019-09-11", "2019-09-25", "2019-10-02", "2019-10-09",
           "2019-10-23", "2019-10-30", "2019-11-06", "2019-11-13", "2019-11-27", "2019-12-04", "2019-12-11",
           "2019-12-24", "2019-12-31", "2018-01-17", "2018-02-14", "2018-03-21", "2018-04-18", "2018-05-16",
           "2018-06-20", "2018-07-18", "2018-08-22", "2018-09-19", "2018-10-17", "2018-11-21", "2018-12-19",
           "2018-01-03", "2018-01-10", "2018-01-24", "2018-01-31", "2018-02-07", "2018-02-21", "2018-02-27",
           "2018-03-07", "2018-03-14", "2018-03-28", "2018-04-04", "2018-04-11", "2018-04-25", "2018-05-02",
           "2018-05-09", "2018-05-23", "2018-05-30", "2018-06-06", "2018-06-13", "2018-06-27", "2018-07-03",
           "2018-07-11", "2018-07-25", "2018-08-01", "2018-08-08", "2018-08-15", "2018-08-29", "2018-09-05",
           "2018-09-12", "2018-09-26", "2018-10-03", "2018-10-10", "2018-10-24", "2018-10-31", "2018-11-07",
           "2018-11-14", "2018-11-28", "2018-12-05", "2018-12-12", "2018-12-26", "2017-01-18", "2017-02-15",
           "2017-03-22", "2017-04-19", "2017-05-17", "2017-06-21", "2017-07-19", "2017-08-16", "2017-09-20",
           "2017-10-18", "2017-11-15", "2017-12-20", "2017-01-04", "2017-01-11", "2017-01-25", "2017-02-01",
           "2017-02-08", "2017-02-22", "2017-03-01", "2017-03-08", "2017-03-14", "2017-03-29", "2017-04-05",
           "2017-04-12", "2017-04-26", "2017-05-03", "2017-05-10", "2017-05-24", "2017-05-31", "2017-06-07",
           "2017-06-14", "2017-06-28", "2017-07-05", "2017-07-12", "2017-07-26", "2017-08-02", "2017-08-09",
           "2017-08-23", "2017-08-30", "2017-09-06", "2017-09-13", "2017-09-27", "2017-10-04", "2017-10-11",
           "2017-10-25", "2017-11-01", "2017-11-08", "2017-11-22", "2017-11-29", "2017-12-06", "2017-12-13",
           "2017-12-27", "2016-01-20", "2016-02-17", "2016-03-16", "2016-04-20", "2016-05-18", "2016-06-15",
           "2016-07-20", "2016-08-17", "2016-09-21", "2016-10-19", "2016-11-16", "2016-12-21", "2016-01-06",
           "2016-01-13", "2016-01-27", "2016-02-03", "2016-02-10", "2016-02-23", "2016-03-02", "2016-03-09",
           "2016-03-23", "2016-03-30", "2016-04-06", "2016-04-13", "2016-04-27", "2016-05-04", "2016-05-11",
           "2016-05-25", "2016-06-01", "2016-06-08", "2016-06-22", "2016-06-29", "2016-07-06", "2016-07-13",
           "2016-07-27", "2016-08-03", "2016-08-10", "2016-08-24", "2016-08-31", "2016-09-07", "2016-09-14",
           "2016-09-28", "2016-10-05", "2016-10-12", "2016-10-26", "2016-11-02", "2016-11-09", "2016-11-23",
           "2016-11-30", "2016-12-07", "2016-12-14", "2016-12-28", "2015-01-21", "2015-02-18", "2015-03-18",
           "2015-04-15", "2015-05-20", "2015-06-17", "2015-07-22", "2015-08-19", "2015-09-16", "2015-10-21",
           "2015-11-18", "2015-12-16", "2015-08-05", "2015-08-12", "2015-08-26", "2015-09-02", "2015-09-09",
           "2015-09-23", "2015-09-30", "2015-10-07", "2015-10-14", "2015-10-28", "2015-11-04", "2015-11-11",
           "2015-11-24", "2015-12-01", "2015-12-09", "2015-12-23", "2015-12-30", "2014-01-22", "2014-02-19",
           "2014-03-18", "2014-04-16", "2014-05-21", "2014-06-18", "2014-07-16", "2014-08-20", "2014-09-17",
           "2014-10-22", "2014-11-19", "2014-12-17", "2013-01-16", "2013-02-13", "2013-03-20", "2013-04-17",
           "2013-05-22", "2013-06-19", "2013-07-17", "2013-08-21", "2013-09-18", "2013-10-16", "2013-11-20",
           "2013-12-18"]
Settle = pd.DataFrame(np.nan, index=range(1000), columns=StrList)
TradeDate = pd.DataFrame(np.nan, index=range(1000), columns=StrList)
Volume = pd.DataFrame(np.nan, index=range(1000), columns=StrList)
for i in range(len(StrList)):
    tic()
    fileID = StrList[i]
    url = 'https://markets.cboe.com/us/futures/market_statistics/historical_data/products/csv/VX/' + fileID
    Future = pd.read_csv(url)
    for j in range(len(Future['Settle'])):
        Settle[StrList[i]][j] = Future['Settle'][j]
        TradeDate[StrList[i]][j] = Future['Trade Date'][j]
        Volume[StrList[i]][j] = Future['Total Volume'][j]
    print(i)
    toc()
Settle.to_pickle("Settle.pkl")
TradeDate.to_pickle("TradeDate.pkl")
Volume.to_pickle("Volume.pkl")
# %% Read pickled files
Settle = pd.read_pickle("Settle.pkl")
TradeDate = pd.read_pickle("TradeDate.pkl")
Volume = pd.read_pickle("Volume.pkl")
# %% Compute tenor
StrList = TradeDate.columns.to_list()
Tenor = pd.DataFrame(np.nan, index=range(1000), columns=StrList)

for i in range(len(StrList)):
    tic()
    contract = pd.to_datetime(StrList[i], yearfirst=True, infer_datetime_format=True)
    Trades = pd.to_datetime(TradeDate[StrList[i]], yearfirst=True, infer_datetime_format=True)
    for j in range(1000):
        Tenor[StrList[i]][j] = (contract - Trades[j]).days
    print(i)
    toc()
# Set day index
min_date = np.datetime64('today')
for i in range(len(StrList)):
    Trades = pd.to_datetime(TradeDate[StrList[i]], yearfirst=True, infer_datetime_format=True)
    min_date = np.min([min_date, Trades.min()])
dates = pd.date_range(min_date, np.datetime64('today'), freq='D').to_numpy(copy=False)
# %% Create tall vectors
tenor = np.floor(Tenor.to_numpy().reshape((Tenor.shape[0] * Tenor.shape[1])) / 7)
price = Settle.to_numpy().reshape((Settle.shape[0] * Settle.shape[1]))
date = pd.to_datetime(pd.Series(TradeDate.to_numpy().reshape((TradeDate.shape[0] * TradeDate.shape[1])))).to_numpy(
    copy=False)
# %% Compute
avg_price = np.zeros((len(dates), 50))
for j in range(50):
    tic()
    for i in range(len(dates)):
        idx = np.logical_and(np.where(date == dates[i], True, False), np.where(tenor == j, True, False))
        if len(price[idx]) == 0:
            avg_price[i, j] = np.nan
        else:
            avg_price[i, j] = np.nanmean(price[idx])
    print(j)
    toc()
mean_price = np.where((avg_price == 0), np.nan, avg_price)
vix_prices = pd.DataFrame(mean_price, index=dates, columns=range(50))
vix_prices.to_pickle('vix_futures_prices_weekly_tenor.pkl')
# %% Pull signal
url = 'http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixcurrent.csv'
VixTbl = pd.read_csv(url, header=1, names=['Date', 'Open', 'High', 'Low', 'Close'], parse_dates=['Date'])
url = 'http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vix3mdailyprices.csv'
Vix3MTbl = pd.read_csv(url, header=2, names=['Date', 'Open', 'High', 'Low', 'Close'], parse_dates=['Date'])
VixTbl['Date'] = pd.to_datetime(VixTbl.Date, infer_datetime_format=True)
Vix3MTbl['Date'] = pd.to_datetime(Vix3MTbl.Date, infer_datetime_format=True)
df = VixTbl.merge(Vix3MTbl, how='inner', on='Date', suffixes=('_vix', '_vix3m'))
df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
df['Signal'] = df['Close_vix3m'] - df['Close_vix']
df.to_pickle('CBOE_VIX_index.pkl')
# %% Create Merged Table
TradingDays = np.intersect1d(dates, df.Date)
signal = df.Signal[np.isin(df.Date.to_numpy(), TradingDays)]
vixprice = vix_prices.to_numpy()[np.isin(dates, TradingDays), :]
InterpolatedSurface = pd.DataFrame(vixprice).interpolate(method='linear', axis=1, limit_direction='both').to_numpy()
vix_returns = pd.DataFrame(np.log(InterpolatedSurface), index=TradingDays, columns=range(50))
vix_returns = vix_returns.diff(periods=1)
vix_returns.to_pickle('vix_returns.pkl')
# %% Pricing the term-structure of vix futures
plt.figure(dpi=800)
plt.plot(TradingDays,
         np.nanmean(InterpolatedSurface[:, 12:36], axis=1) - np.nanmean(InterpolatedSurface[:, 0:5], axis=1), '-k')
plt.plot(TradingDays, signal, ':k')
plt.legend(['slope of VIX futures', 'vix3m - vix'])
plt.title('The Term-Structure of VIX futures')
plt.savefig('vix_futures_slope.png')
plt.show()
# %% Vix futures price surface
fig = go.Figure(data=[go.Surface(z=InterpolatedSurface.transpose())])

fig.update_layout(title='Vix futures prices', autosize=False,
                  width=1200, height=1200,
                  margin=dict(l=65, r=50, b=65, t=90))
fig.show()
# %% SLOPE
SLOPE = np.zeros(len(vix_prices))
for i in range(len(vix_prices)):
    tic()
    data = vix_prices.transpose()[vix_prices.index[i]]
    X = data.index
    X = sm.add_constant(X)
    y = data.values
    try:
        model = sm.RLM(endog=y, exog=X, M=sm.robust.norms.AndrewWave(), missing='drop')
        results = model.fit()
        SLOPE[i] = results.params[1]
    except:
        SLOPE[i] = np.nan
    print(i)
    toc()

SLOPE = pd.DataFrame(SLOPE, index=dates)
SLOPE.to_pickle('SLOPE.pkl')
plt.figure(dpi=900)
plt.plot(SLOPE)
plt.ylabel('SLOPE')
plt.title('Slope of VIX futures term-structure')
plt.savefig('SLOPE.png')
plt.show()
Slope = SLOPE.shift(periods=-1).to_numpy()[np.isin(dates, TradingDays), :]
U = pd.DataFrame(SLOPE.to_numpy()[np.isin(dates, TradingDays), :]).diff(periods=1)
#%% Second pass
Returns = vix_returns.to_numpy()
B = np.zeros((3, 50))
E = np.zeros(50)
for i in range(50):
    tic()
    X = np.vstack((Slope.T, U.T)).T
    X = sm.add_constant(X)
    y = Returns[:, i]
    model = sm.OLS(endog=y, exog=X, missing='drop', hasconst=True)
    results = model.fit()
    for j in range(3):
        B[j, i] = results.params[j]
    print(i)
    E[i] = np.nanmean(np.abs(results.resid))
    toc()
pd.DataFrame(B).to_pickle('B.pkl')
#%% Third pass
X = B[2, :]
X = sm.add_constant(X)
model = sm.OLS(endog=B[0, :], exog=X, missing='none', hasconst=False).fit()
print(model.summary())
lambda0 = model.params[1]

model = sm.OLS(endog=B[1, :], exog=X, missing='none', hasconst=False).fit()
print(model.summary())
Lambda = model.params[1]
#%% Price of risk
PriceOfRisk = pd.DataFrame(Slope).transform(lambda x: lambda0 + Lambda * x)
PriceOfRisk = PriceOfRisk.interpolate(method='linear', axis=0, limit_direction='both')
plt.figure(dpi=900)
plt.plot(dates[np.isin(dates, TradingDays)], PriceOfRisk)
plt.plot(dates[np.isin(dates, TradingDays)], np.nanmean(Returns, axis=1), ':')
plt.title('Price of risk')
plt.savefig('PriceOfRisk.png')
plt.show()
#%% Scatter
plt.figure(dpi=900)
sns.regplot(B[2, :], np.nanmean(Returns, axis=0))
plt.ylabel('mean return')
plt.xlabel('beta (U = change in SLOPE)')
plt.title('Pricing the cross-section')
plt.savefig('Cross-section.png')
plt.show()
x = np.array(range(50))
plt.figure(dpi=900)
sns.regplot(x, np.nanmean(Returns, axis=0))
plt.ylabel('mean return')
plt.xlabel('Tenor in weeks')
plt.title('Pricing the cross-section')
plt.savefig('Cross-section-tenor.png')
plt.show()
# Price of risk
x = np.array(range(50))
Z = sm.nonparametric.lowess(
    endog=np.nanmean(Returns, axis=0),
    exog=x,
    frac=0.12,
    return_sorted=False
)
plt.figure(dpi=900)
plt.plot(
    x,
    np.nanmean(Returns, axis=0),
    linewidth=1,
    color='b',
    linestyle='',
    marker='.'
)
plt.plot(
    x,
    Z,
    linewidth=2.5,
    color='r',
    linestyle='-'
)
plt.xlabel('tenor in weeks')
plt.ylabel('expected return')
plt.title('Term-structure of the price of risk')
plt.savefig('Term-structure-dealer-appetite.png')
plt.show()
#%% Second pass
X = np.vstack((B[2, :].T, np.array(range(50)).T)).T
X = sm.add_constant(X)
model = sm.OLS(endog=B[0, :], exog=X, missing='none', hasconst=False).fit()
print(model.summary())
lambda0 = model.params

model = sm.OLS(endog=B[1, :], exog=X, missing='none', hasconst=False).fit()
print(model.summary())
Lambda = model.params
pd.DataFrame(B).to_pickle('B.pkl')
#%% Controlling for tenor
X = np.array(range(50))
X = sm.add_constant(X)

alpha_tenor = sm.OLS(endog=B[0, :], exog=X, missing='none', hasconst=True).fit()
mu_tenor = sm.OLS(endog=np.nanmean(Returns, axis=0), exog=X, missing='none', hasconst=True).fit()

plt.figure(dpi=400)
sns.regplot(alpha_tenor.resid, mu_tenor.resid)
plt.xlabel('proj(alpha|tenor)')
plt.ylabel('proj(expected returns|tensor)')
plt.title('Zero-beta rate controlling for tenor')
plt.savefig('alpha_orthogonal_to_tenor.png')
plt.show()
X = alpha_tenor.resid
X = sm.add_constant(X)
model = sm.OLS(endog=mu_tenor.resid, exog=X, missing='drop', hasconst=True).fit()
print(model.summary())
#%%
X = np.array(range(50))
X = sm.add_constant(X)
beta_tenor = sm.OLS(endog=B[2, :], exog=X, missing='none', hasconst=True).fit()
mu_tenor = sm.OLS(endog=np.nanmean(Returns, axis=0), exog=X, missing='none', hasconst=True).fit()

plt.figure(dpi=400)
sns.regplot(beta_tenor.resid, mu_tenor.resid)
plt.xlabel('proj(beta|tenor)')
plt.ylabel('proj(expected returns|tenor)')
plt.title('Controlling for tenor')
plt.savefig('beta_orthogonal_to_tenor.png')
plt.show()

X = beta_tenor.resid
X = sm.add_constant(X)
model = sm.OLS(endog=mu_tenor.resid, exog=X, missing='none', hasconst=True).fit()
print(model.summary())
#%%
plt.figure(dpi=900)
sns.regplot(np.array(range(50)), B[2, :])
plt.xlabel('tenor in weeks')
plt.ylabel('beta')
plt.title('Duration and SLOPE betas')
plt.savefig('duration_SLOPE_betas.png')
plt.show()
