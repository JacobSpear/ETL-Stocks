-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/1ux0xJ
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

-- Modify this code to update the DB schema diagram.
-- To reset the sample schema, replace everything with
-- two dots ('..' - without quotes).

CREATE TABLE "tickers" (
    "ticker" VARCHAR(30)   NOT NULL,
    "company_name" Varchar(100)   NOT NULL,
    "sector_id" INT   NOT NULL,
    CONSTRAINT "pk_tickers" PRIMARY KEY (
        "ticker"
     )
);

CREATE TABLE "sectors" (
    "sector_id" INT   NOT NULL,
    "sector" Varchar(30)   NOT NULL,
    CONSTRAINT "pk_sectors" PRIMARY KEY (
        "sector_id"
     )
);

CREATE TABLE "calendar" (
    "date_id" INT   NOT NULL,
    "day" int   NOT NULL,
    "month" int   NOT NULL,
    "day_of_year" int   NOT NULL,
    "day_of_quarter" int   NOT NULL,
    "year" int   NOT NULL,
    CONSTRAINT "pk_calendar" PRIMARY KEY (
        "date_id"
     )
);

CREATE TABLE "stocks" (
    "ticker" Varchar(10)   NOT NULL,
    "date_id" INT   NOT NULL,
    "open_price" FLOAT   NOT NULL,
    "close_price" float   NOT NULL,
    "high_price" FLOAT   NOT NULL,
    "low_price" FLOAT   NOT NULL,
    "volume" int   NOT NULL,
    CONSTRAINT "pk_stocks" PRIMARY KEY (
        "ticker","date_id"
     )
);

CREATE TABLE "currencies" (
    "currency_id" INT   NOT NULL,
    "currency_symbol" Varchar(50)   NOT NULL,
    CONSTRAINT "pk_currencies" PRIMARY KEY (
        "currency_id"
     )
);

CREATE TABLE "exchange_rates" (
    "from_currency_id" INT   NOT NULL,
    "to_currency_id" int   NOT NULL,
    "date_id" INT   NOT NULL,
    "open_value" float   NOT NULL,
    "close_value" float   NOT NULL,
    CONSTRAINT "pk_exchange_rates" PRIMARY KEY (
        "from_currency_id","to_currency_id","date_id"
     )
);

ALTER TABLE "tickers" ADD CONSTRAINT "fk_tickers_sector_id" FOREIGN KEY("sector_id")
REFERENCES "sectors" ("sector_id");

ALTER TABLE "stocks" ADD CONSTRAINT "fk_stocks_ticker" FOREIGN KEY("ticker")
REFERENCES "tickers" ("ticker");

ALTER TABLE "stocks" ADD CONSTRAINT "fk_stocks_date_id" FOREIGN KEY("date_id")
REFERENCES "calendar" ("date_id");

ALTER TABLE "exchange_rates" ADD CONSTRAINT "fk_exchange_rates_from_currency_id" FOREIGN KEY("from_currency_id")
REFERENCES "currencies" ("currency_id");

ALTER TABLE "exchange_rates" ADD CONSTRAINT "fk_exchange_rates_to_currency_id" FOREIGN KEY("to_currency_id")
REFERENCES "currencies" ("currency_id");

ALTER TABLE "exchange_rates" ADD CONSTRAINT "fk_exchange_rates_date_id" FOREIGN KEY("date_id")
REFERENCES "calendar" ("date_id");

