from langchain_groq import ChatGroq

print("✅ Environment Ready")

import os
import sqlite3
import time
import warnings
from datetime import datetime

import pandas as pd
import numpy as np

import yfinance as yf
import ta

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

print("Pandas :", pd.__version__)
print("Numpy  :", np.__version__)
print("YFinance Loaded")
print("TA Loaded")
print("VADER Loaded")
print("✅ Core Libraries Ready")


import os

from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

DB_PATH = "financial_agent.db"

def init_database():

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS portfolio(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        quantity REAL,
        avg_price REAL,
        added_date TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS analysis_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        analysis_date TEXT,
        signal TEXT,
        price REAL,
        rsi REAL
    )
    """)

    conn.commit()
    conn.close()

    print("✅ Database Created")

init_database()

COMPANY_SYMBOL_MAP = {

    "INFOSYS":"INFY.NS",
    "INFY":"INFY.NS",

    "TCS":"TCS.NS",

    "RELIANCE":"RELIANCE.NS",

    "HDFC":"HDFCBANK.NS",

    "ICICI":"ICICIBANK.NS",

    "WIPRO":"WIPRO.NS",

    "AAPL":"AAPL",
    "APPLE":"AAPL",

    "MSFT":"MSFT",
    "MICROSOFT":"MSFT",

    "TSLA":"TSLA",
    "TESLA":"TSLA",

    "NVDA":"NVDA",
    "NVIDIA":"NVDA"
}

def resolve_symbol(user_input):

    key = user_input.upper().strip()

    if key in COMPANY_SYMBOL_MAP:
        return COMPANY_SYMBOL_MAP[key]

    return key

print("✅ Symbol Resolver Ready")

print(resolve_symbol("Infosys"))
print(resolve_symbol("Tesla"))
print(resolve_symbol("TCS"))

def analyze_stock(symbol):

    symbol = resolve_symbol(symbol)

    try:

        stock = yf.Ticker(symbol)

        data = stock.history(period="1y")

        if data.empty:
            return {
                "text": f"No data found for {symbol}",
                "image": None
            }

        data["RSI"] = ta.momentum.RSIIndicator(
            data["Close"],
            window=14
        ).rsi()

        data["MA20"] = data["Close"].rolling(20).mean()
        data["MA50"] = data["Close"].rolling(50).mean()
        data["MA200"] = data["Close"].rolling(200).mean()

        latest = data.dropna().iloc[-1]

        price = round(latest["Close"], 2)
        rsi = round(latest["RSI"], 2)

        ma20 = round(latest["MA20"], 2)
        ma50 = round(latest["MA50"], 2)
        ma200 = round(latest["MA200"], 2)

        if rsi < 30:
            signal = "BUY"

        elif rsi > 70:
            signal = "SELL"

        else:
            signal = "HOLD"

        chart_path = f"{symbol.replace('.','_')}.png"

        plt.figure(figsize=(12,6))

        plt.plot(data.index, data["Close"], label="Price")
        plt.plot(data.index, data["MA20"], label="MA20")
        plt.plot(data.index, data["MA50"], label="MA50")

        plt.legend()

        plt.title(symbol)

        plt.savefig(chart_path)

        plt.close()

        text = f"""
Stock Analysis Report

Symbol : {symbol}

Current Price : {price}

RSI : {rsi}

MA20 : {ma20}
MA50 : {ma50}
MA200 : {ma200}

Signal : {signal}
"""

        return {
            "text": text,
            "image": chart_path
        }

    except Exception as e:

        return {
            "text": str(e),
            "image": None
        }

print("✅ Stock Analysis Ready")

result = analyze_stock("TCS")

print(result["text"])
print(result["image"])

def news_sentiment(symbol):

    symbol = resolve_symbol(symbol)

    analyzer = SentimentIntensityAnalyzer()

    ticker = yf.Ticker(symbol)

    try:
        news = ticker.news
    except:
        return "Unable to fetch news"

    if not news:
        return "No recent news available"

    output = []

    scores = []

    for item in news[:10]:

        try:

            title = item.get("title","")

            sentiment = analyzer.polarity_scores(title)

            compound = sentiment["compound"]

            scores.append(compound)

            if compound > 0.05:
                label = "Positive"

            elif compound < -0.05:
                label = "Negative"

            else:
                label = "Neutral"

            output.append(
                f"{label} | {compound:.2f}\n{title}\n"
            )

        except:
            pass

    if scores:

        avg = sum(scores)/len(scores)

        if avg > 0.05:
            overall = "Bullish"

        elif avg < -0.05:
            overall = "Bearish"

        else:
            overall = "Neutral"

        output.append(
            f"\nOverall Sentiment: {overall}"
        )

    return "\n".join(output)

print("✅ News Sentiment Ready")

print(
    news_sentiment("INFY")
)

def compare_stocks(stock_list):

    symbols = [
        resolve_symbol(x.strip())
        for x in stock_list.split(",")
    ]

    output = []

    output.append("STOCK COMPARISON")
    output.append("=" * 60)

    for symbol in symbols:

        try:

            stock = yf.Ticker(symbol)

            hist = stock.history(period="3mo")

            if hist.empty:
                continue

            info = stock.info

            price = round(
                hist["Close"].iloc[-1],
                2
            )

            pe = info.get(
                "trailingPE",
                "N/A"
            )

            eps = info.get(
                "trailingEps",
                "N/A"
            )

            rsi = ta.momentum.RSIIndicator(
                hist["Close"],
                window=14
            ).rsi().iloc[-1]

            output.append(
f"""
Symbol : {symbol}
Price  : {price}
PE     : {pe}
EPS    : {eps}
RSI    : {rsi:.2f}
"""
            )

        except Exception as e:

            output.append(
                f"{symbol} : {e}"
            )

    return "\n".join(output)

print("✅ Compare Stocks Ready")

print(
    compare_stocks(
        "INFY,TCS,WIPRO"
    )
)

def sip_calculator(monthly_amount, years, annual_return):

    monthly_rate = annual_return / 12 / 100

    months = years * 12

    future_value = monthly_amount * (
        ((1 + monthly_rate) ** months - 1)
        / monthly_rate
    ) * (1 + monthly_rate)

    invested = monthly_amount * months

    gains = future_value - invested

    return f"""
SIP REPORT
================================

Monthly Investment : ₹{monthly_amount:,.0f}

Years              : {years}

Expected Return    : {annual_return}%

Total Invested     : ₹{invested:,.0f}

Future Value       : ₹{future_value:,.0f}

Estimated Profit   : ₹{gains:,.0f}
"""

print("✅ SIP Calculator Ready")

print(
    sip_calculator(
        5000,
        10,
        12
    )
)

def portfolio_add(symbol, qty, price):

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO portfolio
        (symbol, quantity, avg_price, added_date)
        VALUES (?, ?, ?, ?)
        """,
        (
            resolve_symbol(symbol),
            qty,
            price,
            datetime.now().isoformat()
        )
    )

    conn.commit()
    conn.close()

    return "Added Successfully"


def portfolio_view():

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    rows = cur.execute(
        """
        SELECT symbol,
               quantity,
               avg_price
        FROM portfolio
        """
    ).fetchall()

    conn.close()

    if not rows:
        return "Portfolio Empty"

    output = []

    total_invested = 0
    total_value = 0

    for symbol, qty, avg_price in rows:

        try:

            stock = yf.Ticker(symbol)

            hist = stock.history(period="5d")

            current_price = round(
                hist["Close"].iloc[-1],
                2
            )

            invested = qty * avg_price

            current_value = qty * current_price

            pnl = current_value - invested

            total_invested += invested
            total_value += current_value

            output.append(
f"""
{symbol}

Qty : {qty}

Buy : {avg_price}

Current : {current_price}

PnL : {round(pnl,2)}
"""
            )

        except Exception as e:

            output.append(
                f"{symbol} Error {e}"
            )

    output.append(
f"""

========================

Total Invested : {round(total_invested,2)}

Current Value  : {round(total_value,2)}

Net PnL        : {round(total_value-total_invested,2)}
"""
    )

    return "\n".join(output)

print("✅ Portfolio Ready")

print(
    portfolio_add(
        "INFY",
        10,
        1500
    )
)

print(
    portfolio_view()
)

def market_overview():

    indices = {
        "NIFTY50":"^NSEI",
        "SENSEX":"^BSESN",
        "NASDAQ":"^IXIC",
        "S&P500":"^GSPC"
    }

    output = []

    output.append(
        "MARKET OVERVIEW"
    )

    output.append(
        "=" * 50
    )

    for name, ticker in indices.items():

        try:

            hist = yf.Ticker(
                ticker
            ).history(period="5d")

            current = hist["Close"].iloc[-1]

            previous = hist["Close"].iloc[-2]

            change = current - previous

            pct = (
                change / previous
            ) * 100

            output.append(
                f"{name} : {current:.2f} ({pct:.2f}%)"
            )

        except:

            output.append(
                f"{name} unavailable"
            )

    return "\n".join(output)

print("✅ Market Overview Ready")

print(
    market_overview()
)

from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.1
)

print("✅ Groq LLM Ready")

def ask_finagent(question):

    prompt = f"""
You are FinSage.

You are a financial research assistant.

Answer professionally.

Question:

{question}
"""

    response = llm.invoke(prompt)

    return response.content

print("✅ AI Chat Ready")

print(
    ask_finagent(
        "What is RSI in stock market?"
    )
)

import gradio as gr

def ui_stock(symbol):

    result = analyze_stock(symbol)

    return result["text"], result["image"]


def ui_news(symbol):

    return news_sentiment(symbol)


def ui_compare(symbols):

    return compare_stocks(symbols)


def ui_market():

    return market_overview()


def ui_ai(question):

    return ask_finagent(question)

print("✅ UI Functions Ready")

with gr.Blocks() as demo:

    gr.Markdown("# FinSage Financial Research AI")

    with gr.Tab("Stock Analysis"):

        stock_input = gr.Textbox()

        stock_btn = gr.Button("Analyze")

        stock_text = gr.Textbox(lines=20)

        stock_img = gr.Image()

        stock_btn.click(
            ui_stock,
            stock_input,
            [stock_text, stock_img]
        )

    with gr.Tab("News Sentiment"):

        news_input = gr.Textbox()

        news_btn = gr.Button("Analyze")

        news_output = gr.Textbox(lines=20)

        news_btn.click(
            ui_news,
            news_input,
            news_output
        )

    with gr.Tab("Compare"):

        compare_input = gr.Textbox()

        compare_btn = gr.Button("Compare")

        compare_output = gr.Textbox(lines=20)

        compare_btn.click(
            ui_compare,
            compare_input,
            compare_output
        )

    with gr.Tab("Market"):

        market_btn = gr.Button(
            "Refresh"
        )

        market_output = gr.Textbox(
            lines=20
        )

        market_btn.click(
            ui_market,
            outputs=market_output
        )

    with gr.Tab("AI Chat"):

        ai_input = gr.Textbox()

        ai_btn = gr.Button("Ask")

        ai_output = gr.Textbox(
            lines=20
        )

        ai_btn.click(
            ui_ai,
            ai_input,
            ai_output
        )

demo.launch(
    share=True
)
