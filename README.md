# Tech Stock Moving Average Interactive Dashboard

## 1. Problem & User (问题与目标用户)
This app addresses the problem of quickly analyzing stock trends and identifying potential buy/sell signals using Moving Averages. The target users are business students, beginner investors, or financial analysts who need a quick, code-free way to visualize market momentum.

## 2. Data (数据)
- **Source:** Yahoo Finance API (via `yfinance` library).
- **Access Date:** Real-time (Data is fetched dynamically when the user runs the app).
- **Key Fields:** Date, Close Price.

## 3. Methods (主要Python方法)
- **Data Acquisition:** Used `yf.download()` to fetch live market data.
- **Data Cleaning:** Used `pandas.dropna()` to handle missing trading days or `NaN` values.
- **Data Transformation:** Calculated rolling averages using `pandas.DataFrame.rolling(window).mean()`.
- **Visualization:** Built interactive line charts using `plotly.graph_objects` to allow users to hover and inspect specific dates.
- **Deployment:** Built the front-end interface using `Streamlit`.

## 4. Key Findings (核心发现示例)
- AAPL consistently shows strong resilience, but the interactive chart easily reveals short-term volatility.
- By adjusting the SMA inputs (e.g., 10-day vs 50-day), users can clearly visually identify "Golden Cross" (bullish) and "Death Cross" (bearish) moments.
- The tool demonstrates that relying on historical data alone is insufficient, but it provides a solid baseline for quantitative analysis.

## 5. How to run (运行方式)
1. Ensure Python is installed.
2. Run `pip install -r requirements.txt`.
3. Run `streamlit run app.py` in your terminal.

## 6. Product link / Demo (产品与演示链接)
- **App Link:** [在这里贴上你部署后的 Streamlit 链接]
- **Demo Video:** [在这里贴上你录制的 1-3 分钟演示视频链接]

## 7. Limitations & next steps (局限性与改进)
- **Limitations:** The app relies on external API (Yahoo Finance) which may have rate limits. Moving averages are lagging indicators and cannot predict future crashes.
- **Next Steps:** Incorporate more financial metrics (like RSI or MACD) and add a feature to compare two different stocks side-by-side.
