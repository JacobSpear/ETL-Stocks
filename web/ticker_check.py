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

def check_ticker(ticker):
    engine = create_engine(f"postgresql://postgres:{password}@localhost:5432/Stocks")
    conn = engine.connect()
    session = Session(bind=engine)
    Base.metadata.create_all(engine)

    result = session.query(Ticker.ticker).filter(Ticker.ticker==ticker).all()
    if result == []:
        return False
    else:
        return True

    conn.close()