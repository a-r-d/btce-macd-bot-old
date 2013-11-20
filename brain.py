import time
import sys
import os
import pprint
from datetime import datetime
import Quote
import btceapi
import json

exchange_id = 1
currencypair_id = 1
utc_offset = 60 * 60 * 5
active_pair = "ltc_usd"
test_trade = True

apikey = "QLMM16CC-EOXCMTVJ-AIGMSFD4-97Q2HX7G-0Y0KWT8Z"
secret = "74d51f7271b8945f4cfd150202de13bc2aaa4e5579b30003a6d97f8463357b09"

def mainLoop():
    print "looping..."

def info():
    api = btceapi.api( apikey, secret )
    return api.getInfo()

def orders( pair ):
    api = btceapi.api( apikey, secret )
    return api.ActiveOrders( pair )

def isopenorders( infos ):
    return infos["return"]["open_orders"]

def buy( rate, qty ):
    api = btceapi.api( apikey, secret )
    return api.Trade(active_pair, "buy", rate, qty)

def sell( rate, qty ):
    api = btceapi.api( apikey, secret )
    return api.Trade(active_pair, "sell", rate, qty)

def getLTCBal( infos ):
    return infos["return"]["funds"]["ltc"]

def getUSDBal( infos ):
    return infos["return"]["funds"]["usd"]

def getBTCBal( infos ):
    return infos["return"]["funds"]["btc"]

def test():
    global params
    global exchange_id
    global currencypair_id
    
    session = Quote.getSession()
    rows = Quote.getLastQuoteForID(session, currencypair_id, exchange_id)
    quotes = []
    for r in rows: quotes.append(r)
    q = quotes[0]
    print "last: ", float(q.last), q.created

    infos = info()
    #print json.loads(infos)
    print infos
    print infos["return"]["funds"]
    # true, 1 = true or false
    print infos["return"]["open_orders"]
    print "ltc:",getLTCBal(infos)
    print "usd:",getUSDBal(infos)
    print "btc:",getBTCBal(infos)

    time.sleep(0.1)
    if isopenorders(infos) == 1:
        print "orders- ", active_pair, ":", orders(active_pair)
    time.sleep(0.1)

    if test_trade:
        #print buy( 10, 10 )
        time.sleep(0.1)
        print sell( 10, 10 )

if __name__ == "__main__":
    test()
    mainLoop()