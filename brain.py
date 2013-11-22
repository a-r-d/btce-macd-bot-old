import time
import sys
import os
import pprint
from datetime import datetime
import Quote
import btceapi
import json
import sharedlib

exchange_id = 1
currencypair_id = 1
utc_offset = 60 * 60 * 5
active_pair = "ltc_usd"
test_trade = True

safety_on = True # must be false to run trades
short_on_top = None # should be True or False when running
short_avg = "mv_avg_30_min"
long_avg = "mv_avg_600_min"
min_dist_crossover = 10
purse_trade_pct = 0.05 # for testing we trade 5% of the purse

apikey = "QLMM16CC-EOXCMTVJ-AIGMSFD4-97Q2HX7G-0Y0KWT8Z"
secret = "74d51f7271b8945f4cfd150202de13bc2aaa4e5579b30003a6d97f8463357b09"

def mainLoop():
    print "looping..."


def test():
    session = Quote.getSession()
    rows = Quote.getLastQuoteForID(session, currencypair_id, exchange_id)

    quotes = []
    for r in rows: quotes.append(r)
    q = quotes[0]
    print "last: ", float(q.last), q.created

    api = BtceHelper()
    infos = info()
    #print json.loads(infos)
    print infos
    print infos["return"]["funds"]
    # true, 1 = true or false
    print infos["return"]["open_orders"]
    print "ltc:",getLTCBal(infos)
    print "usd:",getUSDBal(infos)
    print "btc:",getBTCBal(infos)

    #if int(isopenorders(infos)) == 1:
    clearallorders()

    #if test_trade:
        #print buy( 10, 10 )
        #print sell( 10, 10 )

if __name__ == "__main__":
    test()
    mainLoop()