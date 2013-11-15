import Quote
import time
import pprint

exchange_id = 1
currencypair_id = 1
utc_offset = 60 * 60 * 5
backtestsecs = 60 * 60 * 24 * 5

amount_usd = 400.0
amount_ltc = 100.0
trade_pct = 0.5
trading_fee = 0.002 ## 0.2 % trading fee
fees_paid_total_usd = 0.0
fees_paid_total_ltc = 0.0

def runTestTrades( crossover ):
    global amount_ltc
    global amount_usd
    global trade_pct
    global trading_fee
    global fees_paid_total_usd
    global fees_paid_total_ltc
    # this will buy LTC at the Ask Price
    quote = crossover["quote"]
    if crossover["buy"]:
        ask = float(quote.ask)
        budget = amount_usd * trade_pct
        qty_purchase = float(budget) / float(ask) # dollars / ltc
        fees_paid_total_usd += qty_purchase * trading_fee
        amount_usd -= budget * trading_fee
        amount_usd -= budget
        amount_ltc += qty_purchase

    # this will sell LTC at the Bid Price
    if crossover["sell"]:
        bid = float(quote.bid)
        budget = amount_ltc * trade_pct
        qty_purchase = float(budget) * float(bid)
        fees_paid_total_ltc += qty_purchase * trading_fee
        amount_ltc -= budget * trading_fee
        amount_ltc -= budget
        amount_usd += qty_purchase


def crossPoints( quotes, mv_avg_short, mv_avg_long ):
    crossovers = []
    if quotes == None:
        return []

    short_on_top =          False
    last_mv_avg_30_min =    getattr(quotes[0], mv_avg_short)
    last_mv_avg_600_min =   getattr(quotes[0], mv_avg_long)
    if last_mv_avg_30_min > last_mv_avg_600_min:
        short_on_top = True

    i = 0
    for q in quotes:
        i += 1
        if i == 1:
            continue
        if getattr(q, mv_avg_short) > getattr(q,mv_avg_long) and short_on_top == False:

            short_on_top = True
            crossovers.append({
                "q_before": quotes[ i-1 ],
                "quote": q,
                "q_after": quotes[ i+1 ],
                "trend":"rising",
                "q_id":q.id,
                "q_last":q.last,
                "buy": True,
                "sell": False
            })
        if getattr(q, mv_avg_short) < getattr(q,mv_avg_long) and short_on_top == True:

            short_on_top = False
            crossovers.append({
                "q_before":quotes[ i-1 ],
                "quote":q,
                "q_after":quotes[i+1],
                "trend":"falling",
                "q_id":q.id,
                "q_last":q.last,
                "buy": False,
                "sell": True
            })

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

        print "running fake trades"
        for crossover in points:
            runTestTrades( crossover )

        print "usd:",amount_usd
        print "ltc:",amount_ltc
        print "fees paid ltc:",fees_paid_total_ltc
        print "fees_paid_total_usd:", fees_paid_total_usd

        print "liquidate value:", (float(quotes[len(quotes) -1].bid) * amount_ltc) + amount_usd
        print "original liquidate value:", (float(quotes[len(quotes) -1].bid) * 100) + 400
    except Exception, e:
        print "Failed on backtest: ", e


def restoreDefaults():
    global amount_usd
    global amount_ltc
    global fees_paid_total_usd
    global fees_paid_total_ltc
    amount_usd = 400.0
    amount_ltc = 100.0
    fees_paid_total_usd = 0.0
    fees_paid_total_ltc = 0.0

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
    backtest( quotes, "mv_avg_30_min", "mv_avg_240_min" )
    restoreDefaults()
    backtest( quotes, "mv_avg_10_min", "mv_avg_600_min" )
    restoreDefaults()
    backtest( quotes, "mv_avg_10_min", "mv_avg_240_min" )
    restoreDefaults()
    backtest( quotes, "mv_avg_60_min", "mv_avg_600_min" )
    restoreDefaults()
    backtest( quotes, "mv_avg_60_min", "mv_avg_240_min" )

if __name__ == "__main__":
    testController()
    