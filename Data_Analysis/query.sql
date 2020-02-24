SELECT ticker,
	date_id, ROUND(CAST(open_price*open_value AS NUMERIC),2) as open_rubles, 
	ROUND(CAST(close_price*open_value AS NUMERIC),2) as close_rubles 
FROM 	
	(SELECT * FROM stocks WHERE ticker='A' AND date_id >= 20200000) AS a_stocks,
	(SELECT open_value 
	 FROM 
		(SELECT date_id, open_value 
		 FROM 
		 	exchange_rates WHERE from_currency_id = 1 AND to_currency_id = 6) 
	 	AS ex_rates
	WHERE ex_rates.date_id >= ALL (SELECT date_id 
								   FROM 
								   	exchange_rates WHERE 
								   	from_currency_id = 1 AND to_currency_id = 6)) 
	as e_rate;


