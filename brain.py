import MySQLdb
import time
import pprint
from datetime import datetime

exchange_id = 1
currencypair_id = 2
utc_offset = 60 * 60 * 5

params = {
    "host":"trollboxarchive.com",
    "user":"cryptotrends",
    "db":"cryptotrends",
    "pass":"crypto123lol"
}

def getLastHour( db, exid, curid ):
    global utc_offset
    offset = 60 * 60 # 60 mins
    t = (time.time() - offset) + utc_offset
    filterdate = datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')

    sql = """
        select * 
        from quote where 
        currencypair_id=%d and 
        exchange_id=%d and 
        created >= '%s'
        """ % ( curid, exid, filterdate)
        
    print sql
    cursor = db.cursor()
    cursor.execute( sql )
    rows = cursor.fetchall()
    #pprint.pprint(rows)

def mainLoop():
    global params
    global exchange_id
    global currencypair_id
    db = None
    try:
        db = MySQLdb.connect(params["host"],params["user"],params["pass"],params["db"])
        thirtyMinMovAvg( db, exchange_id, currencypair_id )
    except Exception, e:
        print "Failed to get mv avg: ", e
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    mainLoop()