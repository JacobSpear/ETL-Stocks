from flask import Flask, render_template, jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///titanic.sqlite")

# # reflect an existing database into a new model
Base = automap_base()
# # reflect the tables
Base.prepare(engine, reflect=True)

# # Save reference to the table
# 
Tickers = Base.classes.tickers

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

@app.route('/endpoint/api/ticker/<ticker_name>.html')
def stocks(ticker_name):
    """Return the stocksdata as json"""

    # return jsonify(stocks_ticker)

    """Fetch the tickers tat match
       the path variable supplied by the user, or a 404 if not."""

    canonicalized = ticker_name.replace(" ", "").lower()
    for ticker in tickers:
        search_term = ticker["ticker"].replace(" ", "").lower()

        if search_term == canonicalized:
            return jsonify(ticker)

    return jsonify({"error": f"Ticker named {ticker_name} not found."}), 404


if __name__ == "__main__":
    app.run(debug=True)
