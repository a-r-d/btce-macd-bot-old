import time
import sys
import os
import pprint
from datetime import datetime
import Quote
import btceapi
import json
import sharedlib

"""
    General Algorithm:

    This is a MACD (Moving average convergance divergance bot)

    1. Start with 20$
    2. If the short MA is above long MA BUY ALL.
    3. Keep checking that short MA is above long MA.
    4. If the short MA dips below long MA SELL ALL.
    5. Keep checking and repeat as necessary.

    The reference currncy is USD.
    The goal is increase USD. 
    We always sell out of the crypto and move to USD when market turns down.
"""

verbose = True

loop_interval = 2 #seconds.
exchange_id = 1
currencypair_id = 3 # btc / usd
#currencypair_id = 1 # ltc / usd

utc_offset = 60 * 60 * 5

active_pair = "btc_usd"
#active_pair = "ltc_usd"

test_trade = True

btc_min_bal = 0.0005
ltc_min_bal = 0.01
usd_min_bal = 0.5

fudge_factor_macd = 0.001 # 0.1% fudge factor here.
buy_percentage = 0.75      # we will buy with 75% of the cash on hand, always sell 100%

safety_on = False # must be false to run trades
short_avg = "mv_avg_30_min"
long_avg = "mv_avg_600_min"


apikey = "ICB6DNFG-MVGUUK6H-EQUTMXJY-B0BWUBDV-QL84UKE0"
secret = "1cbbbfe81eb4e6e1b4c6ff391d311e42bc583ffa1e97fd0f485a0471d123fd73"


def calcSellQtyCoin(quote, fundsCoin):
    # sell @ bid
    print "Funds:", fundsCoin
    price = quote.bid
    #always leave 1%
    qty = fundsCoin * 0.99
    return price, round(qty, 5)


def calcBuyQtyCoin(quote, fundsDollar):
    # buy @ ask
    print "Funds:", fundsDollar
    price = quote.ask
    #always leave 1%
    # buy will be in dollars. 
    qty = fundsDollar * 0.99
    #divide the quantity dollars by the dollar quote coin
    #get the quantity in coins
    return price, round( qty / quote.last, 5)


def mainLoop():
    print "Init Loop..."
    session = Quote.getSession()
    api = sharedlib.BtceHelper(apikey, secret, active_pair)

    while(1):
        if verbose: 
            ts = time.strftime("%b %d %Y %H:%M:%S", time.gmtime(time.time()))
            print "Entering Trade Loop", ts

        quote = Quote.getLastQuoteForIDWithMA(session, currencypair_id, exchange_id)
        short_ma = quote.__dict__[short_avg]
        long_ma = quote.__dict__[long_avg]

        uptrend = None # True = up, False = down, None = no trend
        if short_ma > long_ma and abs(long_ma - short_ma) > quote.last * fudge_factor_macd:
            uptrend = True
        elif short_ma < long_ma and abs(long_ma - short_ma) > quote.last * fudge_factor_macd:
            uptrend = False
        else:
            uptrend = None

        if verbose: 
            print "Quote Date:", quote.created
            print "Short MA:", short_ma
            print "Long MA:", long_ma
            if uptrend:
                print "Uptrend in progress"
            elif uptrend == False:
                print "Downtrend in progress"
            else:
                pct = (abs(long_ma - short_ma) / quote.last) * 100
                print "No trend - within fudge factor percent: ", pct

        orders = api.orders(active_pair)
        if verbose:
            print "Active orders: ", orders
            print "Clearing all orders not filled."
        api.clearallorders(active_pair)

        # this is going to be difficult to generalize:
        info = api.info()
        usd_bal = api.getUSDBal(info)
        btc_bal = api.getBTCBal(info)
        ltc_bal = api.getLTCBal(info)

        if verbose:
            print "Usd:", usd_bal
            print "Btc:", btc_bal
            print "Ltc:", ltc_bal

        ## Specific buy / sell logic for each pair.
        if active_pair == "btc_usd":
            if uptrend == False and btc_bal > btc_min_bal:
                #input=Btc, out=Usd
                price, qty = calcSellQtyCoin(quote, btc_bal)
                if verbose:
                    print "Initiating sell for ", qty, "@", price, " Last:", quote.last
                if not safety_on:
                    result = api.sell(price, qty)
                    print result

            if uptrend == True and usd_bal > usd_min_bal:
                price, qty = calcSellQtyCoin(quote, usd_bal * buy_percentage)
                if verbose:
                    print "Initiating buy for ", qty, "@", price, " Last:", quote.last
                if not safety_on:
                    result = api.buy(price, qty)
                    print result

        if active_pair == "ltc_usd":
            if uptrend == False and ltc_bal > ltc_min_bal:
                price, qty = calcSellQtyCoin(quote, ltc_bal)
                if verbose:
                    print "Initiating sell for ", qty, "@", price, " Last:", quote.last
                if not safety_on:
                    result = api.sell(price, qty)
                    print result

            if uptrend == True and usd_bal > usd_min_bal:
                price, qty = calcSellQtyCoin(quote, usd_bal * buy_percentage)
                if verbose:
                    print "Initiating buy for ", qty, "@", price, " Last:", quote.last
                if not safety_on:
                    result = api.buy(price, qty)
                    print result

        # Sleep after you enter the orders, this is the end.
        time.sleep(loop_interval)
        break



def test():
    session = Quote.getSession()
    q = Quote.getLastQuoteForID(session, currencypair_id, exchange_id)
    print "last: ", float(q.last), q.created

    api = sharedlib.BtceHelper(apikey, secret, currencypair_id)
    info = api.info()

    # true, 1 = true or false
    print info["return"]["open_orders"]
    print "ltc:", api.getLTCBal(info)
    print "usd:", api.getUSDBal(info)
    print "btc:", api.getBTCBal(info)

    #if int(isopenorders(infos)) == 1:
    api.clearallorders()
    #if test_trade:
        #print buy( 10, 10 )
        #print sell( 10, 10 )


if __name__ == "__main__":
    #test()
    mainLoop()
