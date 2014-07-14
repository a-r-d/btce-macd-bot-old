import Quote
import time
import pprint
import traceback

exchange_id = 1
currencypair_id = 3 # 1=usd/ltc, 2=btc/ltc, 3=usd/btc
utc_offset = 60 * 60 * 5
backtestsecs = 60 * 60 * 24 * 1

DEFAULT_amount_usd = 400.0
DEFAULT_amount_ltc = 50.0

amount_usd = DEFAULT_amount_usd
amount_ltc = DEFAULT_amount_ltc
trade_pct = 0.6
trading_fee = 0.002 ## 0.2 % trading fee
fees_paid_total_usd = 0.0
fees_paid_total_ltc = 0.0
trade_records = []

def sellCoins( quote ):
    global amount_ltc
    global amount_usd
    global trade_pct
    global trading_fee
    global fees_paid_total_usd
    global fees_paid_total_ltc
    global trade_records
    
    bid = float(quote.bid)
    budget = amount_ltc * trade_pct
    qty_purchase = float(budget) * float(bid)
    fees_paid_total_ltc += qty_purchase * trading_fee
    amount_ltc -= budget * trading_fee
    amount_ltc -= budget
    amount_usd += qty_purchase

    trade_records.append({
      "type":"sell",
      "qty_coin": budget,
      "total_cost_dollars": qty_purchase,
      "units_budget": quote.units,
      "quote":quote,
      "fees_coin":fees_paid_total_ltc
    })
    return True
  
def buyCoins( quote ):
    global amount_ltc
    global amount_usd
    global trade_pct
    global trading_fee
    global fees_paid_total_usd
    global fees_paid_total_ltc
    global trade_records
    
    ask = float(quote.ask)
    budget = amount_usd * trade_pct
    qty_purchase = float(budget) / float(ask) # dollars / ltc
    fees_paid_total_usd += qty_purchase * trading_fee
    amount_usd -= budget * trading_fee
    amount_usd -= budget
    amount_ltc += qty_purchase
    
    trade_records.append({
      "type":"buy",
      "qty_coin":qty_purchase,
      "total_cost_dollars":budget,
      "units_budget": quote.units,
      "quote":quote,
      "fees_usd":fees_paid_total_usd
    })

    return True

"""
Here the idea is if you go up %5 from the last trade
you will want to sell to lock in a gain.

Rather than using quote.last, we can try to use mv avgs in stop loss also.
"""
def takeProfits( quote, mv_avg_short, mv_avg_long  ):
  global trade_records
  if len(trade_records) > 1:
      last_trade = trade_records[len(trade_records) - 1]
      if last_trade["type"] == "buy":
        pct_diff = float(quote.last) / float(last_trade["quote"].ask)
        #pct_diff = float(getattr(quote, mv_avg_short)) / float(getattr(last_trade["quote"], mv_avg_short))
        if( pct_diff > 1.05 ):
          sellCoins( quote )
          print "triggered a profit taking ", quote.last
          return True
  return False
  

"""
Generally the idea here is if you go down 2% from
the last trade you will want to sell if you are holding.
"""
def stopLoss( quote, mv_avg_short, mv_avg_long  ):
  global trade_records
  if len(trade_records) > 1:
      last_trade = trade_records[len(trade_records) - 1]
      if last_trade["type"] == "buy":
        pct_diff = float(quote.last) / float(last_trade["quote"].ask)
        #pct_diff = float(getattr(quote, mv_avg_short)) / float(getattr(last_trade["quote"], mv_avg_short))
        if( pct_diff < 0.98 ):
          sellCoins( quote )
          print "triggered a stop loss ", quote.last
          return True
  return False

def runTestTrades( quotes, crossovers, mv_avg_short, mv_avg_long  ):
    # this will buy LTC at the Ask Price
    for q in quotes:
        for c in crossovers:
            if c["quote"] == q:
                if c["buy"]:
                    buyCoins( q )
                # this will sell LTC at the Bid Price
                if c["sell"]:
                  sellCoins( q )
        
        stopLoss( q, mv_avg_short, mv_avg_long  )
        takeProfits( q, mv_avg_short, mv_avg_long  )
        
########################################################################
        
def crossPoints( quotes, mv_avg_short, mv_avg_long ):
    crossovers = []
    crossover_min_dist = 15 # essentially 15 minutes
    if quotes == None:
        return []

    short_on_top =          False
    last_mv_avg_30_min =    getattr(quotes[0], mv_avg_short)
    last_mv_avg_600_min =   getattr(quotes[0], mv_avg_long)
    if last_mv_avg_30_min > last_mv_avg_600_min:
        short_on_top = True

    last_crossover = 0
    i = 0
    for q in quotes:
        i += 1
        if i == 1:
            continue
            
        ## this will reduce frequent stupid trades.
        if last_crossover > crossover_min_dist:
          if getattr(q, mv_avg_short) > getattr(q,mv_avg_long) and short_on_top == False:
              short_on_top = True
              crossovers.append({
                  "q_before": quotes[ i-1 ],
                  "quote": q,
                  "q_after": quotes[ i+1 ],
                  "time":q.created,
                  "trend":"rising",
                  "q_id":q.id,
                  "q_last":q.last,
                  "buy": True,
                  "sell": False
              })
              last_crossover = 0
          if getattr(q, mv_avg_short) < getattr(q,mv_avg_long) and short_on_top == True:

              short_on_top = False
              crossovers.append({
                  "q_before":quotes[ i-1 ],
                  "quote":q,
                  "q_after":quotes[i+1],
                  "time":q.created,
                  "trend":"falling",
                  "q_id":q.id,
                  "q_last":q.last,
                  "buy": False,
                  "sell": True
              })
              last_crossover = 0
              
              
        last_crossover += 1
        last_mv_avg_600_min = getattr(q, mv_avg_long)
        last_mv_avg_30_min = getattr(q, mv_avg_short)
    return crossovers


def backtest( quotes, mv_avg_short, mv_avg_long):
    global utc_offset
    global exchange_id
    global currencypair_id
    global backtestsecs
    global amount_usd
    global amount_ltc
    global fees_paid_total_usd
    global fees_paid_total_ltc
    try:
        print "building crossovers for: ", mv_avg_short, " ", mv_avg_long
        points = crossPoints( quotes, mv_avg_short, mv_avg_long )
        
        print "Crossovers:"
        print "Num crossovers: ", len(points)
        pprint.pprint(points);

        print "running fake trades"
        runTestTrades( quotes, points, mv_avg_short, mv_avg_long  )

        print "usd:",amount_usd
        print "ltc:",amount_ltc
        print "fees paid ltc:",fees_paid_total_ltc
        print "fees_paid_total_usd:", fees_paid_total_usd
        print "Starting last quote: ", quotes[0].last
        print "Ending last quote: ", quotes[len(quotes) - 1].last
        liquidate = (float(quotes[len(quotes) -1].bid) * amount_ltc) + amount_usd
        print "liquidate value:", liquidate
        orig = (float(quotes[len(quotes) -1].bid) * DEFAULT_amount_ltc) + DEFAULT_amount_usd
        print "original liquidate value:", orig
        print "Pct diff: ", str(float(liquidate) / float(orig))
    except Exception, e:
        print "Failed on backtest: ", e
        traceback.print_exc()


def restoreDefaults():
    global amount_usd
    global amount_ltc
    global fees_paid_total_usd
    global fees_paid_total_ltc
    global trade_records
    amount_usd = DEFAULT_amount_usd
    amount_ltc = DEFAULT_amount_ltc
    fees_paid_total_usd = 0.0
    fees_paid_total_ltc = 0.0
    trade_records = []

def testController():
    print "begin tests"
    print "pulling quotes"
    session = Quote.getSession()
    rows = Quote.getQuotesNewerThanSecondsCurrEx( 
            session, utc_offset, backtestsecs, 
            currencypair_id, exchange_id)
    quotes = []
    for r in rows: quotes.append(r)

    backtest( quotes, "mv_avg_30_min", "mv_avg_600_min" )
    restoreDefaults()
    #backtest( quotes, "mv_avg_30_min", "mv_avg_240_min" )
    #restoreDefaults()
    #backtest( quotes, "mv_avg_10_min", "mv_avg_600_min" )
    #restoreDefaults()
    #backtest( quotes, "mv_avg_10_min", "mv_avg_240_min" )
    #restoreDefaults()
    #backtest( quotes, "mv_avg_60_min", "mv_avg_600_min" )
    #restoreDefaults()
    #backtest( quotes, "mv_avg_60_min", "mv_avg_240_min" )
    #restoreDefaults()

    # This always loses money lol:
    #backtest( quotes, "mv_avg_10_min", "mv_avg_60_min" )
    #restoreDefaults()

if __name__ == "__main__":
    testController()
    
