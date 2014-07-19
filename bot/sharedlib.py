import Quote
import btceapi

########
def log( thestr ):
    l = open('log.log', 'a')
    ts = time.strftime("%b %d %Y %H:%M:%S", time.gmtime(time.time()))
    l.write(ts + ": " + thestr + "\n")
    l.close()

####
#        yay.
####
class MvAvgAnalysis():
    _currencypair_id    = 1
    _exchange_id        = 1
    _utc_offset         = 60 * 60 * 5

    def __init__( currencypair_id, exchange_id, utc_offset ):
        self._currencypair_id   = currencypair_id
        self._exchange_id       = exchange_id
        self._utc_offset        = utc_offset

    def getCrossovers( timeperiod, short_avg, long_avg ):
        session = Quote.getSession()
        timeperiod = 60 * 30 # 30 mins
        quotes = getQuotesNewerThanSecondsCurrEx(
            session, 
            self._utc_offset, 
            timeperiod, 
            self._currencypair_id, 
            self._exchange_id)
        
        crossovers = []
        i = 0
        # Initialize
        short_on_top_loop = None
        short_avg =  getattr(quotes[0], mv_avg_short)
        long_avg =   getattr(quotes[0], mv_avg_long)
        if short_avg > long_avg:
            short_on_top_loop = True
        else:
            short_on_top_loop = False

        # go over quote sequence
        for q in quotes:
            short_avg =  getattr(quotes[i], mv_avg_short)
            long_avg  =  getattr(quotes[i], mv_avg_long)
            i += 1
            #crossing on top:
            if short_avg > long_avg and short_on_top_loop == False:
                crossovers.append({ "quote":q, "type":"buy" })
                short_on_top_loop = True
                continue
            #crossing underneath:
            if short_avg < long_avg and short_on_top_loop == True:
                crossovers.append({ "quote":q, "type":"sell" })
                short_on_top_loop = False
                continue
                
        return crossovers


#############################################
#
#  Btc-e API helpers
#
#############################################
class BtceHelper():
    _apikey = ""
    _secret = ""
    _active_pair = "btc_usd"

    def __init__( self, apikey, secret, active_pair ):
        self._apikey = apikey
        self._secret = secret
        self._active_pair = active_pair

    def info(self):
        api = btceapi.api( self._apikey, self._secret, True)
        return api.getInfo()

    def orders(self, pair ):
        api = btceapi.api(  self._apikey, self._secret, True )
        return api.ActiveOrders( pair )

    def filterOrdersFromResult(self, result, pair):
        """e.g:
        {u'return': 
            {u'296589812': 
                {u'timestamp_created': 1405298224, u'status': 0, u'rate': 15.0, u'amount': 1.0, 
                u'pair': u'ltc_usd', u'type': u'sell'}}, u'success': 1}
        """
        targets = []
        orders = result["return"]
        for key in orders:
            if orders[key]["pair"] == pair:
                targets.append(orders[key])

        return targets

    def cancelorder(self, pair ):
        api = btceapi.api(  self._apikey, self._secret, True )
        return api.CancelOrder( pair )

    def isopenorders(self, infos ):
        return infos["return"]["open_orders"]

    def clearallorders(self, pair):
        orders_ret = self.orders(pair)
        print orders_ret
        
        if orders_ret.has_key("return"):
            order_list = orders_ret["return"]
            for key in order_list:
                o = order_list[key]
                print "cancelling:", o
                cancel = self.cancelorder(key)
                print cancel
        else:
            print "No orders to clear"
        

    def buy(self, rate, qty ):
        api = btceapi.api( self._apikey, self._secret, True )
        return api.Trade(self._active_pair, "buy", rate, qty)

    def sell(self, rate, qty ):
        api = btceapi.api( self._apikey, self._secret, True )
        return api.Trade(self._active_pair, "sell", rate, qty)

    def getLTCBal(self, infos ):
        return infos["return"]["funds"]["ltc"]

    def getUSDBal(self, infos ):
	try:
		return infos["return"]["funds"]["usd"]
	except Exception,e:
		print str(e)
		print infos
    		return 0

    def getBTCBal(self, infos ):
        return infos["return"]["funds"]["btc"]

    def getbal(self, infos, key ):
        return infos["return"]["funds"][key]






