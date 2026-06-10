# FinSage - Financial Research AI Assistant

## Overview

FinSage is an AI-powered Financial Research Assistant that helps investors analyze stocks, track portfolios, monitor market trends, and gain financial insights through an interactive web interface.

The system combines real-time market data, technical indicators, sentiment analysis, portfolio management, and AI-powered financial question answering into a single platform.

---

## Features

### Stock Analysis

* Real-time stock market data using Yahoo Finance
* Relative Strength Index (RSI) analysis
* Moving Average indicators:

  * MA20
  * MA50
  * MA200
* Buy / Hold / Sell signal generation
* Automated stock price chart visualization

### News Sentiment Analysis

* Fetches latest stock-related news
* Sentiment scoring using VADER Sentiment Analysis
* News classification:

  * Positive
  * Neutral
  * Negative
* Overall Bullish / Bearish sentiment detection

### Stock Comparison

Compare multiple stocks simultaneously using:

* Current Market Price
* RSI
* PE Ratio
* EPS

Example:

INFY, TCS, WIPRO

---

### Portfolio Management

Track personal investments through a built-in SQLite database.

Features:

* Add stock holdings
* Store quantity and purchase price
* View current portfolio value
* Profit/Loss calculation
* Investment summary dashboard

---

### Market Overview

Monitor major market indices including:

* NIFTY 50
* SENSEX
* NASDAQ
* S&P 500

Displays:

* Current Index Value
* Daily Percentage Change

---

### AI Financial Assistant

Powered by:

* Groq API
* Llama 3.1 8B Instant

Capabilities:

* Financial concept explanations
* Investment guidance
* Technical indicator explanations
* General market knowledge
* Financial education support

---

## Tech Stack

### Backend

* Python
* SQLite

### AI & LLM

* LangChain
* LangChain-Groq
* Llama 3.1 8B Instant

### Financial Data

* Yahoo Finance (yFinance)
* TA (Technical Analysis Library)

### Sentiment Analysis

* VADER Sentiment Analyzer

### Visualization

* Matplotlib

### Frontend

* Gradio

---

## Project Structure

```text
financial-research-ai-agent/
│
├── app.py
├── financial_agent.db
├── requirements.txt
├── README.md
│
└── generated_charts/
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/financial-research-ai-agent.git

cd financial-research-ai-agent
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set Groq API Key:

```python
os.environ["GROQ_API_KEY"] = "YOUR_API_KEY"
```

Run the application:

```bash
python app.py
```

---

## Future Improvements

* Fundamental analysis dashboard
* Stock watchlists
* Portfolio diversification insights
* Risk scoring engine
* Financial report analysis
* RAG-based financial document assistant
* Cloud deployment
* Docker support

---

## Version

### v1.0

* Stock Analysis
* News Sentiment Analysis
* Portfolio Tracking
* Market Overview
* AI Financial Assistant
* Gradio Interface

---

## Author

Developed as an AI-powered Financial Research and Investment Analysis Platform using Python, Gradio, Groq LLMs, and Financial Market APIs.
