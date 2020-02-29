# Project-2 Title: Stock-ETL

**Team members:**

* Jacob 
* Luciano
* Mano

### Synopsis:

Extracting the stock data of 500 US companies with 20 years of data by different sectors. We are joining the data with the exchange rate to display the results in one another currency.

###Analyze the stock data for:

1. Highest trading companies by year
2. Highest trading company by volume
3. Highest change in value
4. Lowest change in value
5. Average price by company
6. Address all the above in a foreign currency


https://github.com/JacobSpear/ETL-Stocks (Reository)

https://www.alphavantage.co/documentation/# (Stock data & Exchange rate)

https://datahub.io/core/s-and-p-500-companies#resource-constituents (S&P data for Tickers)


# Technical Documentation:

Stocks -ETL Project
Overview: This documentation is part of the ETL-Stocks Projects. The goal is to extract data from a web site through an API call and ingest data into a database using sqlalchemy and analyze it and provide the data to other prospective analysts through an API interface.
We extracted the Stocks data for 20 years for the S&N 500 companies and analyzed it.  We also extracted the currency exchange rates for the same period. 

The goal is to provide the following stocks information in the different currencies.
1. Highest trading companies by year
2. Highest trading company by volume
3. Highest change in value
4. Lowest change in value
5. Average price by company
6. Address all the above in a foreign currency

## Project details:
The project is split into the following major categories:
1.	Identify the subject area 
2.	Identify the data the data sources
3.	Data extraction and cleansing
4.	Design and build database
5.	Design and build the website

1.	Identify the Subject area: The team reviewed the requirements of the project and considered the following aspects in selecting the project:
a.	Multiple data sources: The data is extracted from two websites as mentioned above in the “Data Sources” section
b.	Calendar table is built in a Spreadsheet
Based on the above data requirements, the team identified Stocks Data analysis with an option to present the information in different currencies.

2.	 Data Sources:
Source of S&P 500 tickers:
https://datahub.io/core/s-and-p-500-companies#resource-constituents
Stocks data and Exchange Rate:
https://www.alphavantage.co/documentation/# (Stock data & Exchange rate)
3.	Data Extraction and Cleansing:
a.	S&P500 Stock Tikers is extracted and loaded in the “Tickers” table
b.	The Stocks data is extracted for the last 20 years and imported in the “Stocks” table. The data is loaded up to the last business day
c.	While the stocks data is extracted the industry to which the Ticker belongs to is added to the “Sectors” table
d.	The calendar data is loaded from the Spreadsheet into the “Calendar” Table
e.	At the end of the process, the code looks for the currencies for which the exchange rates are requested. The exchange rates for the specified currencies is extracted and loaded for the last 20 years.

4.	Design and Build of the data base:
The tables were designed and built as per the ERD diagram shown below
 
5.Design and build of the web site:
htp://127.0.0.1:5000

The stock / currency / data endpoint enables the retrieval of any stock in any currency for any given timeframe. To do so, one should type the following URL on the browser, replacing the keywords encapsulated by < and > with the desired information:
/endpoints/stock_data/<currency_symbol>/<ticker>/<from_date>/<to_date>
Example: htp://127.0.0.1:5000/stock_data/EUR/MSFT/20130000/20191231

## API Documentation:
<h3>Plots</h3>
                              <p>The Plot endopoint enables the visualization of a trendline plot of any company in any year by typing the following URL on the browser, replacing the keywords encapsulated by &lt; and &gt; with the desired information:</p>
                              <code>/plots/&lt;ticker&gt;/&lt;year&gt;</code><br><br>
                              <p> For example, to retrieve the cost of 1 share of the company Agilient Techologies Inc stock in 2019, one should paste the following:</p>
                              <code>/plots/A/2019</code><br><br>
                              <p>The reposnse will look something like this:</p>
                              <img class="img-thumbnail" src="img/A-2019-USD.png">
                            </div>
                        <div class="tab-pane fade" id="profile" role="tabpanel" aria-labelledby="profile-tab">
                        <h3>Data</h3>
                            <p>The stock / currency / data endpoint enables the retrieval of any stock in any currency for any given timeframe. To do so, one should type the following URL on the browser, replacing the keywords encapsulated by &lt; and &gt; with the desired information:</p>
                        <code>/endpoints/stock_data/&lt;currency_symbol&gt;/&lt;ticker&gt;/&lt;from_date&gt;/&lt;to_date&gt;</code><br/><br/>
                            <p> For example, to retrieve stocks from Microsoft in EUR currency during the year of 2019, one should paste the following:</p>
                          <code>/endpoints/stock_data/EUR/MSFT/20170000/20171231</code><br/><br/>
                            <p>The return would then be:</p>
                            <pre id="json">
                              "Request_Data": {
                                "Currency": "EUR", 
                                "From_Date": "20170000", 
                                "Ticker": "MSFT", 
                                "To_Date": "20171231"
                              }, 
                              "Stock_Data": {
                                "2017-01-03": {
                                  "close_price": "60.11 EUR", 
                                  "high_price": "60.05 EUR", 
                                  "low_price": "59.37 EUR", 
                                  "open_price": "60.0 EUR", 
                                  "volume": "20694101"
                                }, 
                                "2017-01-04": {
                                  "close_price": "59.39 EUR", 
                                  "high_price": "60.27 EUR", 
                                  "low_price": "59.67 EUR", 
                                  "open_price": "60.01 EUR", 
                                  "volume": "21339969"
                                }, 
                                "2017-01-05": {
                                  "close_price": "58.75 EUR", 
                                  "high_price": "59.73 EUR", 
                                  "low_price": "59.13 EUR", 
                                  "open_price": "59.29 EUR", 
                                  "volume": "24875968"
                                }, (...) </pre>

## Images:
![Trend Line for Amazon Stock for the year 2018](AMZN-2018-USD.png)
![API Documentation Page](API_Documentation_Page.png)
![API Documentation Page](Documentation_Page.png)
![ERD ETL-Stocks](ERD ETL-Stocks.png)
![Index Page](Index_Page.png)

 
