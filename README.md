# Bitcoin Price Analysis Dashboard

A professional, interactive Streamlit app for analyzing Bitcoin prices using real-time and historical data. The dashboard provides insightful visualizations, moving averages, daily returns, and allows custom date range analysis.

## Features
- **Real-time Bitcoin price** (CoinGecko API)
- **Historical price data** (Yahoo Finance via yfinance, from 2020 to present)
- **Line chart of closing prices**
- **Moving averages (20-day, 50-day)**
- **Histogram of daily returns**
- **Custom date range selection**
- **Minimalistic, data-focused UI**
- **Sidebar for input options**

## Tech Stack
- Python 3.8+
- Streamlit
- pandas, numpy
- matplotlib, seaborn
- yfinance
- requests

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd bitcoin
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**
   ```bash
   streamlit run bitcoin_price_analysis.py
   ```

## Usage
- Use the sidebar to select your desired date range (from 2020 to present).
- View real-time price, historical trends, moving averages, and daily returns.
- Analyze the data table and quick analysis for insights.

## Deployment
- Deploy directly on [Streamlit Cloud](https://streamlit.io/cloud) or any platform supporting Streamlit apps.

## Notes
- Data is for informational purposes only and does not constitute financial advice.
- Ensure a stable internet connection for real-time and historical data fetching.

---

**Author:** Your Name 