# 📈 Nifty Option Signal App

This Streamlit-based web app provides real-time Nifty 50 trading signals using an AI-powered algorithm, visualizes key market data, and helps traders make fast decisions during market hours.

### 🌐 Live App
[Click here to view live](https://niftyoptionapp-kfglgg8d65tpgka7cga7ze.streamlit.app/)

---

## 🔧 Features

- ✅ **Buy/Sell Signals** with Entry, Target, and Stoploss
- 🟡 **Option Chain Integration**
- 📉 **5-Minute Price Movement**
- 🔄 **Auto Refresh every 5 minutes** (only during market hours)
- 🕰️ **Fallback Cache Data** when live market data is unavailable

---

## 🛠️ Tech Stack

- `Streamlit` – Frontend UI
- `YFinance` & `NSE India` – Market data API
- `Pandas` & `NumPy` – Data processing
- `Matplotlib` – Chart visualizations
- `Requests`, `Datetime`, `JSON` – Backend logic

---

## 🧠 AI-Based Signal Logic

- The algorithm compares **Open-High-Low-Close** patterns
- Generates signals based on **momentum, support/resistance zones**, and **short-term trends**
- Targets and Stoploss are calculated using volatility ranges

---

## ⚠️ Notes

- 📊 Works **only during Indian market hours** (9:15 AM – 3:30 PM IST)
- If market is closed, fallback data or cached price is shown
- All data is fetched from **free public APIs**

---

## 🖥️ Local Installation

```bash
git clone https://github.com/your-username/nifty-option-signal-app.git
cd nifty-option-signal-app
pip install -r requirements.txt
streamlit run app.py
