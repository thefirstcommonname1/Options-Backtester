import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()
c.execute("select * from optionmodel where symbol_id = 2 and implied_volatility > 0.20 and type = 'put' and strike_price < underlying_price;")

rows = c.fetchall()
strike_price = []
expiration = []
data_date = []
ask_price = []
bid_price = []
for row in rows:
	strike_price.append(row[15])
	expiration.append(row[8][:-9]) #removing the time element from the data
	data_date.append(row[2])
	ask_price.append(int(row[3]))
	bid_price.append(int(row[5]))

number_of_winners = 0
number_of_trades = 0
profit_per_trade = []

sold_at = 0
bought_at = 0
for i in range(len(ask_price)):
	sold_at = (ask_price[i] + bid_price[i]) // 2
	number_of_trades += 1
	for j in range(i+1, len(ask_price)):
		#incase the data is being collected at different times in the same day
		if (strike_price[i] == strike_price[j]) and (expiration[i] == expiration[j]) and (data_date[i] != data_date[j]):
			if ((ask_price[j] + bid_price[j]) // 2) <= (0.5 * sold_at):
				bought_at = (ask_price[j] + bid_price[j] // 2)
				profit = sold_at - bought_at
				profit_per_trade.append(profit)
				if profit > 0:
					number_of_winners += 1
				break
		elif (strike_price[i] == strike_price[j]) and (data_date[i] == data_date[j]):
			bought_at = (ask_price[j] + bid_price[j]) // 2
			profit = sold_at - bought_at
			if profit > 0:
				number_of_winners += 1
				break

print("Number_of_winners:", number_of_winners)
print("Number_of_trades:", number_of_trades)

