from time import sleep
import requests
import pandas as pd
import matplotlib.pyplot as plt
from config import password

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, func, create_engine, ForeignKey
from sqlalchemy.orm import Session
import datetime as dt

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

base_url = "https://www.alphavantage.co/query?"

def alpha_stock_request(function,symbol):
    return requests.get(base_url + f"function={function}&symbol={symbol}&outputsize=full&apikey={api_key}")

def alpha_currency_request(function,from_symbol,to_symbol):
    return requests.get(base_url + f"function={function}&from_symbol={from_symbol}&to_symbol={to_symbol}" +
    "&outputsize=full&apikey={api_key}")

def add_currency(new_currency):
    """description here"""

    engine2 = create_engine(f"postgresql://postgres:{password}@localhost:5432/Stocks")
    conn2 = engine2.connect()
    session2 = Session(bind=engine2)
    Base.metadata.create_all(engine2)
    
    from_call = alpha_currency_request('FX_DAILY',new_currency,'USD').json()
    if list(from_call.keys())[0]=='Error Message':
        return "404 Error: Currency Does Not Exist"
    else:
        to_call = alpha_currency_request('FX_DAILY','USD',new_currency).json()
        
        new_entry = Currency(currency_symbol = new_currency)
        session2.add(new_entry)
        session2.commit()
        
        new_id = session2.query(Currency.currency_id).filter(Currency.currency_symbol == new_currency).one()[0]
        us_id = session2.query(Currency.currency_id).filter(Currency.currency_symbol == "USD").one()[0]
        
        today = from_call['Meta Data']['5. Last Refreshed']
        from_data = from_call['Time Series FX (Daily)']
        to_data = to_call['Time Series FX (Daily)']
        
        for x in from_data:
            if x != today:
                open_value = from_data[x]['1. open']
                close_value = from_data[x]['4. close']
                year , month , day = x.split("-")
                date_ref = int(year + month + day)
                new_rate = Exchange_rate(from_currency_id = new_id,
                              to_currency_id = us_id,
                              date_id = date_ref,
                              open_value = open_value,
                              close_value = close_value)
                session2.add(new_rate)
                session2.commit()
        
        for x in to_data:
            if x != today:
                open_value = to_data[x]['1. open']
                close_value = to_data[x]['4. close']
                year , month , day = x.split("-")
                date_ref = int(year + month + day)
                new_rate = Exchange_rate(from_currency_id = us_id,
                              to_currency_id = new_id,
                              date_id = date_ref,
                              open_value = open_value,
                              close_value = close_value)
                session2.add(new_rate)
                session2.commit()
                
        sleep(2)
        conn2.close()
        return "success"

def upsert_currency(currency):
    #Create Connection
    engine = create_engine(f"postgresql://postgres:{password}@localhost:5432/Stocks")
    conn = engine.connect()
    session = Session(bind=engine)
    Base.metadata.create_all(engine)

    C = Currency
    result = session.query(C.currency_symbol,C.currency_id).filter(C.currency_symbol== currency).all()
    sleep(2)
    conn.close()
    if result == []:
        attempt = add_currency(currency)
        if attempt == "success":
            return True
        else: 
            return False
    else:
        return True


    