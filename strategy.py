import pandas as pd
import Binance
import math
from talib import EMA, ATR, RSI, TRIX, MA
import requests

class start:
	def __init__(self, symbol, quote, interval):
		self.symbol = symbol
		self.quote = quote
		self.base = symbol[:-4]
		self.interval = interval
		self.df = self.getData()
		self.fire = self.strategy()

	def getData(self):
		candles = Binance.client.get_klines(symbol=self.symbol, interval=self.interval)

		#Sorting candlestick using Pandas
		df = pd.DataFrame(candles)
		df = df.drop(range(6, 12), axis=1)

		# put in dataframe and clean-up
		col_names = ['time', 'open', 'high', 'low', 'close', 'volume']
		df.columns = col_names
		# transform values from strings to floats
		for col in col_names:
			df[col] = df[col].astype(float)

		return df

	def strategy(self):

		df = self.df
		volume2 = float(df['volume'].iloc[-2])

		v2 = MA(df['volume'], timeperiod=14)
		v2= float(v2.iloc[-2])

		open = float(df['open'].iloc[-2])
		close = float(df['close'].iloc[-2])
		#Note: all setup for limited orders above are based on ATR indicator. If you want to customise it, just subtract or add up current value with the number you like
		#example: longSL = float(floatPrecision((current - current*0.1), self.step_size)) set stop loss at 1% of entry price

		"""Set up your strategy here 
		Conditions for trading"""

		break1 = volume2 > 2*v2
		giatang = close>1.04*open
		giagiam=close<0.94*open

		#############################################


		def telegram_bot_sendtext (bot_message):

			bot_token = '1970658422:AAF5WJBVkVmB6EU66H5DY7LWXxEDaq447pw'
			bot_chatID = '1159104289'
			send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + \
				'&parse_mode=MarkdownV2&text='+ bot_message
			response = requests.get(send_text)

			return response.json()

		while break1 == True:
			try:
				telegram_bot_sendtext (self.symbol+ ' last vol breakout mavol14')
				break
			except Exception as e:
				print('Error occured while trying to place LONG order: {}'.format(e))

		while giatang == True:
			try:
				telegram_bot_sendtext (self.symbol+ ' gia tang')
				break
			except Exception as e:
				print('Error occured while trying to place LONG order: {}'.format(e))
		
		while giagiam == True:
			try:
				telegram_bot_sendtext (self.symbol+ ' giagiam')
				break
			except Exception as e:
				print('Error occured while trying to place LONG order: {}'.format(e))


"""Scan and place order for all symbols available on market
WARNING: This option may triggering liquidation if you don't have a clear 
capital management strategy or your account is too small,
better go with 1 or 2 symbol if you are a beginner
"""
# OPTION 1
def run():
    quote = 'USDT'
   
    t = Binance.client.get_exchange_info()

    for i in t['symbols']:
        if i['symbol'].endswith(quote):
            start(i['symbol'], quote, interval= '5m')