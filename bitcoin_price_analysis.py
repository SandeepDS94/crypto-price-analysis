import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import requests
from datetime import datetime, timedelta

# Set Streamlit page config
st.set_page_config(
    page_title="Crypto Price Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set Seaborn style
sns.set_style("whitegrid")
sns.set_palette("deep")

# ----------------------
# Coin List and Mapping
# ----------------------
# List of at least 30 popular coins with their CoinGecko and Yahoo Finance tickers
COINS = [
    {"name": "Bitcoin", "cg_id": "bitcoin", "yf_ticker": "BTC-USD", "symbol": "₿"},
    {"name": "Ethereum", "cg_id": "ethereum", "yf_ticker": "ETH-USD", "symbol": "Ξ"},
    {"name": "Tether", "cg_id": "tether", "yf_ticker": "USDT-USD", "symbol": "$"},
    {"name": "BNB", "cg_id": "binancecoin", "yf_ticker": "BNB-USD", "symbol": "BNB"},
    {"name": "Solana", "cg_id": "solana", "yf_ticker": "SOL-USD", "symbol": "◎"},
    {"name": "XRP", "cg_id": "ripple", "yf_ticker": "XRP-USD", "symbol": "XRP"},
    {"name": "USDC", "cg_id": "usd-coin", "yf_ticker": "USDC-USD", "symbol": "$"},
    {"name": "Dogecoin", "cg_id": "dogecoin", "yf_ticker": "DOGE-USD", "symbol": "Ð"},
    {"name": "Cardano", "cg_id": "cardano", "yf_ticker": "ADA-USD", "symbol": "₳"},
    {"name": "Avalanche", "cg_id": "avalanche-2", "yf_ticker": "AVAX-USD", "symbol": "AVAX"},
    {"name": "Shiba Inu", "cg_id": "shiba-inu", "yf_ticker": "SHIB-USD", "symbol": "SHIB"},
    {"name": "TRON", "cg_id": "tron", "yf_ticker": "TRX-USD", "symbol": "TRX"},
    {"name": "Polkadot", "cg_id": "polkadot", "yf_ticker": "DOT-USD", "symbol": "DOT"},
    {"name": "Chainlink", "cg_id": "chainlink", "yf_ticker": "LINK-USD", "symbol": "LINK"},
    {"name": "Polygon", "cg_id": "matic-network", "yf_ticker": "MATIC-USD", "symbol": "MATIC"},
    {"name": "Litecoin", "cg_id": "litecoin", "yf_ticker": "LTC-USD", "symbol": "Ł"},
    {"name": "Bitcoin Cash", "cg_id": "bitcoin-cash", "yf_ticker": "BCH-USD", "symbol": "BCH"},
    {"name": "Uniswap", "cg_id": "uniswap", "yf_ticker": "UNI1-USD", "symbol": "UNI"},
    {"name": "Internet Computer", "cg_id": "internet-computer", "yf_ticker": "ICP-USD", "symbol": "ICP"},
    {"name": "Stellar", "cg_id": "stellar", "yf_ticker": "XLM-USD", "symbol": "XLM"},
    {"name": "OKB", "cg_id": "okb", "yf_ticker": "OKB-USD", "symbol": "OKB"},
    {"name": "Monero", "cg_id": "monero", "yf_ticker": "XMR-USD", "symbol": "XMR"},
    {"name": "Ethereum Classic", "cg_id": "ethereum-classic", "yf_ticker": "ETC-USD", "symbol": "ETC"},
    {"name": "Cosmos", "cg_id": "cosmos", "yf_ticker": "ATOM-USD", "symbol": "ATOM"},
    {"name": "Filecoin", "cg_id": "filecoin", "yf_ticker": "FIL-USD", "symbol": "FIL"},
    {"name": "Aptos", "cg_id": "aptos", "yf_ticker": "APT-USD", "symbol": "APT"},
    {"name": "Lido DAO", "cg_id": "lido-dao", "yf_ticker": "LDO-USD", "symbol": "LDO"},
    {"name": "Hedera", "cg_id": "hedera-hashgraph", "yf_ticker": "HBAR-USD", "symbol": "HBAR"},
    {"name": "Arbitrum", "cg_id": "arbitrum", "yf_ticker": "ARB-USD", "symbol": "ARB"},
    {"name": "VeChain", "cg_id": "vechain", "yf_ticker": "VET-USD", "symbol": "VET"},
    {"name": "Maker", "cg_id": "maker", "yf_ticker": "MKR-USD", "symbol": "MKR"},
    {"name": "Optimism", "cg_id": "optimism", "yf_ticker": "OP-USD", "symbol": "OP"},
]

COIN_NAME_TO_META = {c["name"]: c for c in COINS}

# ----------------------
# Data Fetching Functions
# ----------------------
def fetch_realtime_price(coin_cg_id):
    """Fetch real-time coin price from CoinGecko API."""
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_cg_id}&vs_currencies=usd"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data[coin_cg_id]['usd']
    except Exception as e:
        st.error(f"Error fetching real-time price: {e}")
        return None

def fetch_historical_data(yf_ticker, start_date, end_date):
    """Fetch historical coin data from Yahoo Finance using yfinance."""
    ticker = yf.Ticker(yf_ticker)
    df = ticker.history(start=start_date, end=end_date)
    df = df[['Close']]
    df.index = pd.to_datetime(df.index)
    return df

# ----------------------
# Data Processing Functions
# ----------------------
def calculate_moving_averages(df, windows=[20, 50]):
    """Add moving averages to DataFrame."""
    for window in windows:
        df[f"MA_{window}"] = df['Close'].rolling(window=window).mean()
    return df

def calculate_daily_returns(df):
    """Calculate daily returns."""
    df['Daily Return'] = df['Close'].pct_change()
    return df

# ----------------------
# Plotting Functions
# ----------------------
def plot_closing_price(df, coin_name):
    """Plot historical closing prices."""
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df.index, df['Close'], label='Close', color='#1f77b4')
    ax.set_title(f'{coin_name} Closing Price', fontsize=16)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.legend()
    plt.tight_layout()
    return fig

def plot_moving_averages(df, coin_name):
    """Plot closing price with moving averages."""
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df.index, df['Close'], label='Close', color='#1f77b4', linewidth=1.5)
    if 'MA_20' in df.columns:
        ax.plot(df.index, df['MA_20'], label='20-day MA', color='#ff7f0e', linewidth=1)
    if 'MA_50' in df.columns:
        ax.plot(df.index, df['MA_50'], label='50-day MA', color='#2ca02c', linewidth=1)
    ax.set_title(f'{coin_name} Price with Moving Averages', fontsize=16)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.legend()
    plt.tight_layout()
    return fig

def plot_daily_returns_hist(df, coin_name):
    """Plot histogram of daily returns."""
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df['Daily Return'].dropna(), bins=50, kde=True, color='#1f77b4', ax=ax)
    ax.set_title(f'Histogram of {coin_name} Daily Returns', fontsize=16)
    ax.set_xlabel('Daily Return')
    ax.set_ylabel('Frequency')
    plt.tight_layout()
    return fig

# ----------------------
# Streamlit UI
# ----------------------

def main():
    # Sidebar - Coin and Date range selection
    st.sidebar.title("Crypto Price Analysis")
    st.sidebar.markdown("""
    Analyze price trends, moving averages, and daily returns for your favorite cryptocurrencies with real-time and historical data.
    """)
    coin_name = st.sidebar.selectbox("Select Coin", [c["name"] for c in COINS], index=0)
    coin_meta = COIN_NAME_TO_META[coin_name]
    min_date = datetime(2020, 1, 1)
    max_date = datetime.today()
    default_start = min_date
    default_end = max_date
    start_date = st.sidebar.date_input("Start Date", default_start, min_value=min_date, max_value=max_date)
    end_date = st.sidebar.date_input("End Date", default_end, min_value=min_date, max_value=max_date)
    if start_date > end_date:
        st.sidebar.error("Start date must be before end date.")
        return

    # Fetch data
    with st.spinner('Fetching data...'):
        df = fetch_historical_data(coin_meta["yf_ticker"], start_date, end_date + timedelta(days=1))
        df = calculate_moving_averages(df)
        df = calculate_daily_returns(df)
        realtime_price = fetch_realtime_price(coin_meta["cg_id"])

    # Main page
    st.title(f"{coin_meta['symbol']} {coin_name} Price Dashboard")
    st.markdown("""
    <style>
    .metric-label { font-size: 1.2em; }
    .metric-value { font-size: 2.5em; font-weight: bold; color: #1f77b4; }
    </style>
    """, unsafe_allow_html=True)

    # Real-time price metric
    col1, col2 = st.columns([1, 3])
    with col1:
        if realtime_price:
            st.metric(label=f"Current {coin_name} Price (USD)", value=f"${realtime_price:,.2f}")
        else:
            st.warning("Real-time price unavailable.")
    with col2:
        st.write("")

    # Plots
    st.subheader("Historical Closing Price")
    st.pyplot(plot_closing_price(df, coin_name))

    st.subheader("Price with Moving Averages (20, 50 days)")
    st.pyplot(plot_moving_averages(df, coin_name))

    st.subheader("Histogram of Daily Returns")
    st.pyplot(plot_daily_returns_hist(df, coin_name))

    # Data Table
    st.subheader("Data Table (Last 10 Days)")
    st.dataframe(df.tail(10).style.format({"Close": "${:,.2f}", "MA_20": "${:,.2f}", "MA_50": "${:,.2f}", "Daily Return": "{:.2%}"}))

    # Analysis
    st.subheader("Quick Analysis")
    if not df.empty:
        last_close = df['Close'].iloc[-1]
        ma20 = df['MA_20'].iloc[-1]
        ma50 = df['MA_50'].iloc[-1]
        st.markdown(f"- **Last Close:** ${last_close:,.2f}")
        st.markdown(f"- **20-day MA:** ${ma20:,.2f}")
        st.markdown(f"- **50-day MA:** ${ma50:,.2f}")
        if last_close > ma20 > ma50:
            st.success("Bullish trend: Price above both moving averages.")
        elif last_close < ma20 < ma50:
            st.error("Bearish trend: Price below both moving averages.")
        else:
            st.info("Mixed trend: Price between moving averages.")
    else:
        st.warning("No data available for the selected range.")

    st.markdown("---")
    st.markdown("""
    **Disclaimer:** This dashboard is for informational purposes only and does not constitute financial advice.
    """)

if __name__ == "__main__":
    main() 