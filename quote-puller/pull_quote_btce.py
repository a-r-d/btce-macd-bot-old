#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import urllib2
import urllib
import MySQLdb
import json
import random
import pprint

DB_HOST = "localhost"
DB_USER = ""
DB_PASS = ""
DB_NAME = "cryptotrends"

local = True
if local:
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASS = "test"
    DB_NAME = "cryptotrends"


BTC_2_USD = "https://btc-e.com/api/2/btc_usd/ticker"
LTC_2_USD = "https://btc-e.com/api/2/ltc_usd/ticker"
LTC_2_BTC = "https://btc-e.com/api/2/ltc_btc/ticker"
BTC_2_EUR = "https://btc-e.com/api/2/btc_eur/ticker"
PPC_2_BTC = "https://btc-e.com/api/2/ppc_btc/ticker"
NMC_2_BTC = "https://btc-e.com/api/2/nmc_btc/ticker"
TRC_2_BTC = "https://btc-e.com/api/2/trc_btc/ticker"
NVC_2_BTC = "https://btc-e.com/api/2/nvc_btc/ticker"
FTC_2_BTC = "https://btc-e.com/api/2/ftc_btc/ticker"
XPM_2_BTC = "https://btc-e.com/api/2/xpm_btc/ticker"
NVC_2_USD = "https://btc-e.com/api/2/nvc_usd/ticker"
NMC_2_USD = "https://btc-e.com/api/2/nmc_usd/ticker"

class BTCeQuote():
    def __init__(self, jsondata):
        try:
            dat = json.loads( jsondata )
            #print "Data: ", dat
            #print "high:", dat["ticker"]["high"]
            self.high = float(dat["ticker"]["high"])
            self.low = float(dat["ticker"]["low"])
            self.last = float(dat["ticker"]["last"])
            self.vol = float(dat["ticker"]["vol"])
            self.buy = float(dat["ticker"]["buy"])
            self.sell = float(dat["ticker"]["sell"])
            self.avg = float(dat["ticker"]["avg"])
        except Exception,e:
            print e
            self.errors = True
    errors = False
    high = 0
    low = 0
    last = 0
    vol = 0
    buy = 0
    sell = 0
    avg = 0

def getURL(url):
    return url + "/?cache_buster=" + str(time.time()) + str(random.random())

def get_quote( url_base ):
    url = getURL(url_base)
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'cryptotrends data retrieval job')
    response = urllib2.urlopen(req)
    txt = response.read()
    #print txt
    quote = BTCeQuote(txt)
    pprint.pprint(vars(quote))

    try:
        db = MySQLdb.connect(DB_HOST,DB_USER,DB_PASS,DB_NAME)
        cursor = db.cursor()
        try:
            #using prepared statementS:
            sql_string = ""
            ## 1
            if url_base == LTC_2_USD:
                sql_string = """INSERT INTO quote 
                        (exchange_id, currencypair_id, created, units, last, high, low, bid, ask, volume, average) 
                    VALUES (1, 1, NOW(), 'USD', %f, %f, %f, %f, %f, %f, %f)"""
            ## 2
            elif url_base == BTC_2_USD:
                sql_string = """INSERT INTO quote 
                        (exchange_id, currencypair_id, created, units, last, high, low, bid, ask, volume, average) 
                    VALUES (1, 3, NOW(), 'USD', %f, %f, %f, %f, %f, %f, %f)"""
            ## 3
            elif url_base == LTC_2_BTC:
                sql_string = """INSERT INTO quote 
                        (exchange_id, currencypair_id, created, units, last, high, low, bid, ask, volume, average) 
                    VALUES (1, 2, NOW(), 'BTC', %f, %f, %f, %f, %f, %f, %f)"""
            ## 4
            elif url_base == BTC_2_EUR:
                sql_string = """INSERT INTO quote 
                        (exchange_id, currencypair_id, created, units, last, high, low, bid, ask, volume, average) 
                    VALUES (1, 4, NOW(), 'EUR', %f, %f, %f, %f, %f, %f, %f)"""
            ## 5
            elif url_base == NMC_2_BTC:
                sql_string = """INSERT INTO quote 
                        (exchange_id, currencypair_id, created, units, last, high, low, bid, ask, volume, average) 
                    VALUES (1, 6, NOW(), 'BTC', %f, %f, %f, %f, %f, %f, %f)"""
            ## 6
            elif url_base == NVC_2_BTC:
                sql_string = """INSERT INTO quote 
                        (exchange_id, currencypair_id, created, units, last, high, low, bid, ask, volume, average) 
                    VALUES (1, 8, NOW(), 'BTC', %f, %f, %f, %f, %f, %f, %f)"""
            ## 7
            elif url_base == TRC_2_BTC:
                sql_string = """INSERT INTO quote 
                        (exchange_id, currencypair_id, created, units, last, high, low, bid, ask, volume, average) 
                    VALUES (1, 7, NOW(), 'BTC', %f, %f, %f, %f, %f, %f, %f)"""
            ## 8
            elif url_base == PPC_2_BTC:
                sql_string = """INSERT INTO quote 
                        (exchange_id, currencypair_id, created, units, last, high, low, bid, ask, volume, average) 
                    VALUES (1, 5, NOW(), 'BTC', %f, %f, %f, %f, %f, %f, %f)"""
            ## 9
            elif url_base == FTC_2_BTC:
                sql_string = """INSERT INTO quote 
                        (exchange_id, currencypair_id, created, units, last, high, low, bid, ask, volume, average) 
                    VALUES (1, 9, NOW(), 'BTC', %f, %f, %f, %f, %f, %f, %f)"""
            ## 10
            elif url_base == XPM_2_BTC:
                sql_string = """INSERT INTO quote 
                        (exchange_id, currencypair_id, created, units, last, high, low, bid, ask, volume, average) 
                    VALUES (1, 10, NOW(), 'BTC', %f, %f, %f, %f, %f, %f, %f)"""
            ## 11
            elif url_base == NVC_2_USD:
                sql_string = """INSERT INTO quote 
                        (exchange_id, currencypair_id, created, units, last, high, low, bid, ask, volume, average) 
                    VALUES (1, 11, NOW(), 'USD', %f, %f, %f, %f, %f, %f, %f)"""
            ## 12
            elif url_base == NMC_2_USD:
                sql_string = """INSERT INTO quote 
                        (exchange_id, currencypair_id, created, units, last, high, low, bid, ask, volume, average) 
                    VALUES (1, 12, NOW(), 'USD', %f, %f, %f, %f, %f, %f, %f)"""
            
            else:
                raise Exception("Uknown url base. Maybe you forgot to add it.")

            sql = sql_string % (
                quote.last,
                quote.high,
                quote.low,
                quote.sell,
                quote.buy,
                quote.vol,
                quote.avg
            )
            cursor.execute(sql)
            db.commit()

        except Exception, e:
            print "Failed to INSERT: ", e
            db.rollback()
        finally:
            db.close()
    except Exception, e:
        print "Failed to connect to DB: ", e

        
def cycle():
    # we sleep so I don't catch a ban. 
    # 9 * 5 = 45
    # 9 * 3 = 27
    # 9 * 2 = 18
    #1
    get_quote( LTC_2_USD )
    time.sleep(2)
    #2
    get_quote( BTC_2_USD )
    time.sleep(2)
    #3
    """
    get_quote( LTC_2_BTC )
    time.sleep(2)
    #4
    get_quote( BTC_2_EUR )
    time.sleep(2)
    #5
    get_quote( NMC_2_BTC )
    time.sleep(2)
    #6
    get_quote( NVC_2_BTC )
    time.sleep(2)
    #7
    get_quote( TRC_2_BTC )
    time.sleep(2)
    #8
    get_quote( PPC_2_BTC )
    time.sleep(2)
    #9
    get_quote( FTC_2_BTC )
    time.sleep(2)
    #10
    get_quote( XPM_2_BTC )
    time.sleep(2)
    #11
    get_quote( NVC_2_BTC )
    time.sleep(2)
    #12
    get_quote( NMC_2_USD )
    time.sleep(2)
    """
            
     
if __name__ == '__main__':
    # cron job on for one minute. We pull quotes 3x a minute.
    cycle()
    #cycle()
    #cycle()
    print "done."
