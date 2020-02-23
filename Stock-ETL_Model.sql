CREATE TABLE "tickers" (
    "ticker" VARCHAR(30) PRIMARY KEY,
    "company_name" Varchar(100) NOT NULL,
    "sector_id" INT
);

CREATE TABLE "sectors" (
    "sector_id" SERIAL PRIMARY KEY,
    "sector" Varchar(30) NOT NULL
);

CREATE TABLE "calendar" (
    "date_id" INT PRIMARY KEY,
    "day" int   NOT NULL,
    "month" int   NOT NULL,
    "day_of_year" int   NOT NULL,
    "day_of_quarter" int   NOT NULL,
    "year" int   NOT NULL
);

CREATE TABLE "stocks" (
    "ticker" Varchar(30)  NOT NULL,
    "date_id" INT  NOT NULL,
    "open_price" FLOAT  NOT NULL,
    "close_price" FLOAT  NOT NULL,
    "high_price" FLOAT   NOT NULL,
    "low_price" FLOAT   NOT NULL,
    "volume" BIGINT   NOT NULL,
    CONSTRAINT "pk_stocks" PRIMARY KEY (
        "ticker","date_id"
     )
);

CREATE TABLE "currencies" (
    "currency_id" SERIAL PRIMARY KEY,
    "currency_symbol" Varchar(50)   NOT NULL
);

CREATE TABLE "exchange_rates" (
    "from_currency_id" INT   NOT NULL,
    "to_currency_id" INT  NOT NULL,
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

