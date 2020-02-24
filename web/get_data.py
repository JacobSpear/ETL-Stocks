from time import sleep
import requests
import pandas as pd
import matplotlib.pyplot as plt
from config import password
from date_handler import date_id_sequence, to_string

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, func, create_engine, ForeignKey, text, and_
from sqlalchemy.orm import Session
import datetime as dt
from flask import jsonify

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
try:
    conn.close()
except NameError:
    pass


def get_data(currency,ticker,from_date,to_date):
    engine = create_engine(f"postgresql://postgres:{password}@localhost:5432/Stocks")
    conn = engine.connect()
    session = Session(bind=engine)
    Base.metadata.create_all(engine)

    currency_id = session.query(Currency.currency_id).filter(Currency.currency_symbol == currency).one()[0]

    E = Exchange_rate
    max_date = max([x[0] for x in 
     session.query(Exchange_rate.date_id).filter(and_(E.from_currency_id == 1,E.to_currency_id == currency_id)).all()])

    ex_rates = session.query(Exchange_rate.date_id,Exchange_rate.open_value).filter(and_(E.from_currency_id==1,
                                                                              E.to_currency_id==currency_id)).subquery()

    e_rate = session.query(ex_rates.c.open_value).filter(ex_rates.c.date_id>=max_date).subquery()

    data = session.query(Stock.ticker,
                  Stock.date_id,
                  (Stock.open_price*e_rate).label(f"open_{ticker}_{currency}"),
                   (Stock.high_price*e_rate).label(f"high_{ticker}_{currency}"),
                    (Stock.low_price*e_rate).label(f"low_{ticker}_{currency}"),
                  (Stock.close_price*e_rate).label(f"close_{ticker}_{currency}"),
                    Stock.volume).\
                    filter(and_(Stock.ticker==ticker,
                                Stock.date_id >= from_date,
                                Stock.date_id < to_date)).all()

    data_json = {}
    data_json['Request_Data'] = {'Ticker' : ticker , 
                                 'Currency' : currency , 
                                 'From_Date' : from_date , 
                                 'To_Date': to_date}

    data_json['Stock_Data'] = {}

    for x in data:
        data_json['Stock_Data'][to_string(x[1])] = {'open_price' : str(round(x[2],2))+f' {currency}',
                                                       'high_price' : str(round(x[3],2))+f' {currency}',
                                                       'low_price' : str(round(x[4],2))+f' {currency}',
                                                       'close_price' : str(round(x[5],2))+f' {currency}',
                                                       'volume' : str(x[6])}
                                                
    conn.close()
    return data_json


    

    