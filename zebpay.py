import urllib, json

import time
from exchanges.bitfinex import Bitfinex
import subprocess as s


# url_inr = "https://live.zebapi.com/api/v2/ticker?currencyCode=INR"
# url_usd = "https://live.zebapi.com/api/v2/ticker?currencyCode=USD"

url_ltc = "https://api.cryptowat.ch/markets/bitfinex/ltcusd/price"

# max_num = 820000
# min_num = 800000

# exchange_rate_orig = 74.46

curr_price_orig = int(Bitfinex().get_current_price())

min_ltc = max_ltc = 0
min_btc = max_btc = 0
init_flag = 1

curr_price_ltc = 125

while (1):
	sound_flag = 0
	# response_inr = urllib.urlopen(url_inr)
	# response_usd = urllib.urlopen(url_usd)
	response_ltc = urllib.urlopen(url_ltc)

	# data_inr = json.loads(response_inr.read())
	# data_usd = json.loads(response_usd.read())
	data_ltc = json.loads(response_ltc.read())

	# mk_inr = data_inr['market']
	# mk_usd = data_usd['market']

	ltc_price = data_ltc['result']['price']

	# exchange_rate = mk_inr/mk_usd

	# sell_price = data_inr['sell']

	curr_price = int(Bitfinex().get_current_price())
	ltc_buy_price = int(ltc_price)*64 + 1000
	btc_buy_price = curr_price*64 + 50000

	if init_flag:
		init_flag = 0
		min_btc = max_btc = curr_price
		min_ltc = max_ltc = ltc_price

	if max_ltc < ltc_price :
		max_ltc = ltc_price

	if min_ltc > ltc_price :
		min_ltc = ltc_price

	if max_btc < curr_price :
		max_btc = curr_price

	if min_btc > curr_price :
		min_btc = curr_price

	# print "Selling Price : {} Exchange Rate : {} Bitcoin Price : {}".format(sell_price,exchange_rate, curr_price)

	print "Max BTC : {} Min BTC : {}".format(max_btc,min_btc)
	print "Max LTC : {} Min LTC : {}".format(max_ltc,min_ltc)

	print "Bitcoin Price : {} BTC buy price : {} LTC price : {} LTC Buy price : {} ".format(curr_price,btc_buy_price,ltc_price,ltc_buy_price)

	# if abs(curr_price - curr_price_orig) > 50 :
	# 	s.call(['notify-send','Bitcoin Price Update',str(curr_price)])
	# 	curr_price_orig = curr_price
	# 	sound_flag = 1

	# if abs(curr_price_ltc - ltc_price) > 2 :
	# 	s.call(['notify-send','Lite coin Price Update',str(ltc_price)])
	# 	curr_price_ltc = ltc_price
	# 	sound_flag = 1

	if (max_btc - min_btc) > 50 :
		s.call(['notify-send','Bitcoin Price Update',str(curr_price)])
		max_btc = min_btc = curr_price
		sound_flag = 1

	if (max_ltc - min_ltc) > 2 :
		s.call(['notify-send','Lite coin Price Update',str(ltc_price)])
		max_ltc = min_ltc = ltc_price
		sound_flag = 1


	if sound_flag:
		for i in range(3):
			s.call(["ffplay", "-nodisp", "-autoexit","beep-06.wav"])

	time.sleep(5)