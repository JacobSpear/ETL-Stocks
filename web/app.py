from flask import Flask, render_template, jsonify, url_for
import numpy as np
import os

from time import sleep
import requests
import pandas as pd
import matplotlib.pyplot as plt
from config import password
from image import one_year_open
from get_data import get_data

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, func, create_engine, ForeignKey
from sqlalchemy.orm import Session
import datetime as dt


#################################################
# Database Setup
#################################################
#Create ORM Classes
Base=declarative_base()


class Sector(Base):
    __tablename__="sectors"
    sector_id = Column(Integer, primary_key=True)
    sector = Column(String(30))

class Ticker(Base):
    __tablename__="tickers"
    ticker = Column(String(30),primary_key=True)
    company_name = Column(String(100))
    sector_id = Column(Integer, ForeignKey("sectors.sector_id"))

class Currency(Base):
    __tablename__="currencies"
    currency_id = Column(Integer, primary_key=True)
    currency_symbol = Column(String(50))

class Date(Base):
    __tablename__="calendar"
    date_id = Column(Integer,primary_key=True)
    day = Column(Integer)
    month = Column(Integer)
    day_of_year = Column(Integer)
    day_of_quarter = Column(Integer)
    year = Column(Integer)

class Stock(Base):
    __tablename__="stocks"
    ticker = Column(String(30),ForeignKey("tickers.ticker"),primary_key=True)
    date_id = Column(Integer,ForeignKey("calendar.date_id"),primary_key=True)
    open_price = Column(Float())
    close_price = Column(Float())
    high_price = Column(Float())
    low_price = Column(Float())
    volume = Column(Integer)
    
class Exchange_rate(Base):
    __tablename__="exchange_rates"
    from_currency_id = Column(Integer, ForeignKey("currencies.currency_id"),primary_key=True)
    to_currency_id = Column(Integer, ForeignKey("currencies.currency_id"),primary_key=True)
    date_id = Column(Integer, ForeignKey("calendar.date_id"),primary_key=True)
    open_value = Column(Float())
    close_value = Column(Float())
    
#Create Connection
engine = create_engine(f"postgresql://postgres:{password}@localhost:5432/Stocks")
conn = engine.connect()
session = Session(bind=engine)
Base.metadata.create_all(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__, static_url_path='')


#################################################
# Flask Routes
#################################################


@app.route("/")
def index():

    return render_template("index.html")

@app.route("/documentation.html")
def documentation():

    return render_template("documentation.html")

@app.route("/analysis")
def analysis():
   return render_template("analysis.html")

@app.route("/report")
def report():
    return render_template("report.html")

@app.route("/endpoints")
def endpoints():
    return render_template("endpoints.html")

@app.route("/endpoints/tickers")
def tickers_endpoints():
        # Create our session (link) from Python to the DB
        session = Session(engine)

        """Return a list of all passenger names"""
        # Query all passengers
        results = session.query(tickers.ticker).all()

        session.close()

        # Convert list of tuples into normal list
        all_tickers = list(np.ravel(results))

        return jsonify(all_names)

@app.route("/endpoints/stock_data/<currency_symbol>/<ticker_name>/<from_date>/<to_date>")
def stock_currency(currency_symbol,ticker_name,from_date,to_date):
    return jsonify(get_data(currency_symbol,ticker_name,from_date,to_date))


@app.route('/endpoint/api/ticker/<ticker_name>')
def stocks(ticker_name):
    """Return the stocksdata as json"""

    # return jsonify(stocks_ticker)

    """Fetch the tickers that match
       the path variable supplied by the user, or a 404 if not."""

    canonicalized = ticker_name.replace(" ", "").lower()
    for ticker in tickers:
        search_term = ticker["ticker"].replace(" ", "").lower()

        if search_term == canonicalized:
            return jsonify(ticker)

    return jsonify({"error": f"Ticker named {ticker_name} not found."}), 404

@app.route('/plots/<ticker_name>/<year>')
def ticker_year_plot(ticker_name,year):
    img_url = one_year_open(ticker_name,year)
    return render_template("plots.html",img_url = url_for('static',filename=img_url))

if __name__ == "__main__":
    app.run(debug=True)
