# Updated Nifty Option Signal App with Corrected Sell Signal Logic and Enhanced Chart
import yfinance as yf
import pandas as pd
from datetime import datetime, time, timedelta
import streamlit as st
import requests
from bs4 import BeautifulSoup
import altair as alt

st.set_page_config(page_title="Nifty Option Signal App", layout="centered")
st.title("\U0001F4CA Nifty Option Signal App")

# ------------------ ⏰ Market Timings ------------------
market_open = time(9, 15)
market_close = time(15, 30)
now = datetime.now().time()
market_is_open = market_open <= now <= market_close

# ------------------ 📦 Load Nifty Data ------------------
@st.cache_data(ttl=60)
def get_nifty_data():
    try:
        end = datetime.now()
        start = end - timedelta(days=2)
        data = yf.download("^NSEI", start=start, end=end, interval="5m", progress=False, auto_adjust=False)
        return data
    except Exception as e:
        st.error(f"⚠️ Failed to fetch live data: {e}")
        return pd.DataFrame()

data = get_nifty_data()

# ------------------ 📌 Latest Price ------------------
if not data.empty:
    try:
        latest_price = float(data['Close'].values[-1].item())
        st.metric("📌 Latest Nifty Price", f"₹{latest_price:.2f}")
    except Exception as e:
        st.error(f"⚠️ Unable to extract latest price: {e}")

    if not market_is_open:
        st.warning("📉 Market is currently closed. Data may not be live.")

    # ------------------ 📈 Chart ------------------
    st.subheader("Price Movement (5-min intervals)")
    try:
        chart_data = data.reset_index()[['Datetime', 'Close']].rename(columns={'Datetime': 'Time'})
        chart = alt.Chart(chart_data).mark_line().encode(
            x='Time:T',
            y=alt.Y('Close:Q', scale=alt.Scale(domain=[latest_price - 30, latest_price + 30])),
            tooltip=['Time:T', 'Close:Q']
        ).properties(
            width=700,
            height=300,
            title="Nifty Price Movement (5-min intervals)"
        )
        st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        st.warning(f"⚠️ Failed to display chart: {e}")

    # ------------------ 🟢 Buy/Sell Signals ------------------
    st.markdown("---")
    st.subheader("🟢 Buy/Sell Signals")

    def generate_signals(df):
        df = df.copy()
        df['SMA5'] = df['Close'].rolling(window=5).mean()
        df['SMA20'] = df['Close'].rolling(window=20).mean()
        df['Signal'] = 0
        df.loc[df['SMA5'] > df['SMA20'], 'Signal'] = 1
        df.loc[df['SMA5'] < df['SMA20'], 'Signal'] = -1
        return df

    signal_df = generate_signals(data)
    latest_signal = signal_df['Signal'].values[-1]

    if latest_signal == 1:
        st.success("🟢 Buy Signal")
    elif latest_signal == -1:
        st.error("🔴 Sell Signal")
    else:
        st.info("🟡 No Clear Signal")

    # ------------------ 🎯 Target / Stoploss ------------------
    st.markdown("---")
    st.subheader("🎯 Target / Stoploss")

    def calculate_target_stoploss(df, multiplier=1.5, signal=0):
        df = df.copy()
        df['H-L'] = df['High'] - df['Low']
        df['H-PC'] = abs(df['High'] - df['Close'].shift(1))
        df['L-PC'] = abs(df['Low'] - df['Close'].shift(1))
        df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
        df['ATR'] = df['TR'].rolling(window=14).mean()

        latest_atr = float(df['ATR'].dropna().values[-1])
        latest_close = float(df['Close'].dropna().values[-1].item())

        if signal == 1:  # Buy Signal
            target = latest_close + (multiplier * latest_atr)
            stoploss = latest_close - (multiplier * latest_atr)
        elif signal == -1:  # Sell Signal
            target = latest_close - (multiplier * latest_atr)
            stoploss = latest_close + (multiplier * latest_atr)
        else:
            target = latest_close
            stoploss = latest_close

        return round(target, 2), round(stoploss, 2)

    try:
        target, stoploss = calculate_target_stoploss(data, signal=latest_signal)
        st.write(f"🎯 **Target**: ₹{target}")
        st.write(f"💪 **Stoploss**: ₹{stoploss}")
    except Exception as e:
        st.warning(f"⚠️ Could not calculate Target/Stoploss: {e}")

    # ------------------ 📟 Option Chain Integration ------------------
    st.markdown("---")
    st.subheader("📟 Option Chain (NIFTY)")

    @st.cache_data(ttl=300)
    def fetch_option_chain():
        try:
            url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
            headers = {"User-Agent": "Mozilla/5.0"}
            with requests.Session() as s:
                s.get("https://www.nseindia.com", headers=headers)
                res = s.get(url, headers=headers)
            data = res.json()
            df = pd.json_normalize(data['records']['data'])
            df = df[['strikePrice', 'CE.openInterest', 'PE.openInterest']].dropna()
            df.columns = ['Strike Price', 'Call OI', 'Put OI']
            return df
        except Exception as e:
            st.warning(f"⚠️ Option chain fetch failed: {e}")
            return pd.DataFrame()

    option_chain_df = fetch_option_chain()
    if not option_chain_df.empty:
        st.dataframe(option_chain_df.head(10))
    else:
        st.info("🔄 Option Chain not available currently.")
else:
    st.error("❌ No data available. Please check your internet connection or try again later.")

# ------------------ 🪠 Developer Note ------------------
st.caption("Built with ❤️ by Vimalraj | Powered by Yahoo Finance & NSE")