import pandas as pd
import streamlit as st
import yfinance as yf


# fix yfinance MultiIndex problem
def fix_yfinance_columns(df):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


# load yfinance market data function
@st.cache_data
def load_market_data(ticker, period):
    df = yf.download(ticker, period=period)
    # fix y finance columns
    df = fix_yfinance_columns(df)
    # calculate daily return
    df["Daily Return"] = df["Close"].pct_change() * 100
    # calculate 50-day moving average
    df["50 Day MA"] = df["Close"].rolling(window=50).mean()
    # calculate 200-day moving average
    df["200 Day MA"] = df["Close"].rolling(window=200).mean()
    # calculate 30-day volatility
    df["30 Day Volatility"] = df["Daily Return"].rolling(window=30).std()
    df["Previous Peak"] = df["Close"].cummax()
    df["Drawdown"] = ((df["Close"] - df["Previous Peak"]) / df["Previous Peak"]) * 100
    df["30 Day Return"] = (df["Close"].pct_change(periods=30)) * 100
    df["Rolling Sharpe Ratio"] = (
            (df["Daily Return"].rolling(window=30).mean()) / (df["Daily Return"].rolling(window=30).std())
    )
    df["Annualized Volatility"] = df["30 Day Volatility"] * (252 ** 0.5)
    return df


@st.cache_data
def load_economic_data(_fred, series_code):
    series = _fred.get_series(series_code)
    # convert the fred series to a dataframe with one column called Economic Indicator
    df = series.to_frame(name="Economic Indicator")
    # Converts monthly/quarterly data into daily frequency and fills missing days with the latest known value.
    df = df.resample("D").ffill()
    return df


def get_latest_value(series):
    clean_series = series.dropna()

    if clean_series.empty:
        return None

    return clean_series.iloc[-1].item()