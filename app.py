import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta

# 1. 页面设置
st.set_page_config(page_title="Tech Stock Tracker", layout="wide")
st.title("📈 科技股趋势与移动平均线交互分析工具")
st.markdown("本工具旨在帮助金融初学者和个人投资者分析主要科技股的趋势，并使用简单的移动平均线(SMA)寻找潜在的买卖信号。")

# 2. 侧边栏交互输入
st.sidebar.header("User Settings / 用户设置")
ticker = st.sidebar.selectbox("Choose a Stock Ticker (选择股票):", ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"])
days_back = st.sidebar.slider("Days of Historical Data (历史天数):", 30, 365, 180)
sma_short = st.sidebar.number_input("Short SMA (短期均线天数):", min_value=5, max_value=20, value=10)
sma_long = st.sidebar.number_input("Long SMA (长期均线天数):", min_value=21, max_value=100, value=50)

# 3. 数据获取与清洗 (Python Data Work)
@st.cache_data
def load_data(ticker_symbol, period):
    end_date = date.today()
    start_date = end_date - timedelta(days=period)
    data = yf.download(ticker_symbol, start=start_date, end=end_date)
    # 数据清洗：处理缺失值
    data.dropna(inplace=True)
    return data

data = load_data(ticker, days_back)

if not data.empty:
    # 4. 数据转换与分析: 计算移动平均线
    data[f'SMA_{sma_short}'] = data['Close'].rolling(window=sma_short).mean()
    data[f'SMA_{sma_long}'] = data['Close'].rolling(window=sma_long).mean()

    # 5. 核心洞察与指标展示
    st.subheader(f"{ticker} 关键指标摘要")
    col1, col2, col3 = st.columns(3)
    
    # 提取收盘价序列并转换为纯数字，增加 squeeze() 防止格式报错
    close_prices = data['Close'].squeeze()
    latest_close = float(close_prices.iloc[-1])
    previous_close = float(close_prices.iloc[-2])
    price_change = latest_close - previous_close
    
    col1.metric("最新收盘价 (Latest Close)", f"${latest_close:.2f}", f"{price_change:.2f}")
    
    # 提取均线并展示
    sma_short_val = float(data[f'SMA_{sma_short}'].squeeze().iloc[-1])
    sma_long_val = float(data[f'SMA_{sma_long}'].squeeze().iloc[-1])
    
    col2.metric(f"{sma_short}天短期均线", f"${sma_short_val:.2f}")
    col3.metric(f"{sma_long}天长期均线", f"${sma_long_val:.2f}")

    # 6. 交互式可视化 (使用 Plotly)
    st.subheader("📊 价格趋势与交互式均线图")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=close_prices, mode='lines', name='收盘价 (Close)', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=data.index, y=data[f'SMA_{sma_short}'].squeeze(), mode='lines', name=f'{sma_short}-Day SMA', line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=data.index, y=data[f'SMA_{sma_long}'].squeeze(), mode='lines', name=f'{sma_long}-Day SMA', line=dict(color='green')))
    
    fig.update_layout(xaxis_title="Date", yaxis_title="Price (USD)", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    # 显示原始清洗后的数据 (供用户下载或检查)
    with st.expander("查看原始数据表格 (View Raw Data)"):
        st.dataframe(data.tail(10))
else:
    st.error("无法获取数据，请检查网络或更换股票代码。")
