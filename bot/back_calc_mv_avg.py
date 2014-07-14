#!/usr/bin/python
import sys
import MySQLdb
import MySQLdb.cursors
import time
import pprint
from datetime import datetime
import calendar

"""
Usage:

back_calc_mv_avg.py [exchange_id] [currencypair_id] [seconds]

Example:

back_calc_mv_avg.py 1 3 86000


"""

exchange_id = 1
currencypair_id = 3 # 3 = btc / usd
utc_offset = 60 * 60 * 5
how_far_back = 60 * 60 * 6 

params = {
    "host":"trollboxarchive.com",
    "user":"cryptotrendsrem",
    "db":"cryptotrends",
    "pass":"qazremoteuser123"
}

def rowTimeToTimestamp( row ):
    timestruct = time.strptime(row["created"], '%Y-%m-%d %H:%M:%S')
    timestamp = calendar.timegm(timestruct)
    return timestamp

def timestampTomMysql( tstamp ):
    return datetime.fromtimestamp(tstamp).strftime('%Y-%m-%d %H:%M:%S')

def calcMvAvg(db, exid, curid, rows, field, offset, rowset_mod):
    global params
    global utc_offset
    for row in rows:
        # delay to test.
        if row[field] == None:
            # do all of these one by one:
            db = None
            try:
                db = MySQLdb.connect(
                params["host"],
                params["user"],
                params["pass"],
                params["db"], 
                cursorclass=MySQLdb.cursors.DictCursor)
                print "Working on row: ", row["id"]
                #pprint.pprint(row)
                st = (time.mktime(row["created"].timetuple()) - offset)
                startdate = timestampTomMysql( st )
                ed = (time.mktime(row["created"].timetuple()))
                enddate = timestampTomMysql(ed )
                print startdate, enddate, st, ed

                sql = """
                    select * 
                    from quote where 
                    currencypair_id=%d and 
                    exchange_id=%d and 
                    created >= '%s' and
                    created <= '%s'
                    """ % ( curid, exid, startdate, enddate)
                # I think this makes data too choppy :( 
                #
                #if rowset_mod != -1:
                #    sql = """
                #      select * 
                #      from quote where 
                #      currencypair_id=%d and 
                #      exchange_id=%d and 
                #      created >= '%s' and 
                #      created <= '%s' and 
                #      MOD(id,%d)=0
                #     """ % ( curid, exid, startdate, enddate, rowset_mod)
                    
                print "Gettting subrows: ", sql

                cursor = db.cursor()
                cursor.execute( sql )
                sumrows = cursor.fetchall()
                print "Number results: ", len(sumrows)
                sums = 0.0
                for srow in sumrows:
                    sums += float(srow["last"])

                avg = str(float(sums / float(len(sumrows))))
                sql = """
                    update quote set %s=%s where id=%s
                    """ % ( field, avg, row["id"])
                print "update mv avg: ", sql
                cursor.execute( sql )
                db.commit()
            except Exception, e:
                print "Whoa, moving avg calc blew up! " + str(e)
                db.rollback()  

def tenMins(db, exid, curid, rows  ):
    print "Doing 10 minute mv avg"
    calcMvAvg(db, exid, curid, rows, "mv_avg_10_min", 60 * 10, -1 );

def thirtyMins(db, exid, curid, rows  ):
    print "Doing 30 minute mv avg"
    calcMvAvg(db, exid, curid, rows, "mv_avg_30_min", 60 * 30, -1 );

def sixtyMins(db, exid, curid, rows  ):
    print "Doing 60 minute mv avg"
    calcMvAvg(db, exid, curid, rows, "mv_avg_60_min", 60 * 60, -1 );

def twoFortyMins(db, exid, curid, rows  ):
    print "Doing 240 minute mv avg"
    calcMvAvg(db, exid, curid, rows, "mv_avg_240_min", 60 * 60 * 4, -1 );

def sixHundyMins(db, exid, curid, rows  ):
    print "Doing 600 minute mv avg"
    calcMvAvg(db, exid, curid, rows, "mv_avg_600_min", 60 * 600, -1 );

def oneDay(db, exid, curid, rows  ):
    print "Doing 1 day mv avg"
    calcMvAvg(db, exid, curid, rows, "mv_avg_1_day", 60 * 60 * 24, 25);

def twoDay(db, exid, curid, rows  ):
    print "Doing 2 day mv avg"
    calcMvAvg(db, exid, curid, rows, "mv_avg_2_day", 60 * 60 * 24 * 2, 100);

def fiveDay(db, exid, curid, rows  ):
    print "Doing 5 day mv avg"
    calcMvAvg(db, exid, curid, rows, "mv_avg_5_day", 60 * 60 * 24 * 5, 200);

def tenDay(db, exid, curid, rows  ):
    print "Doing 10 day mv avg"
    calcMvAvg(db, exid, curid, rows, "mv_avg_10_day", 60 * 60 * 24 * 10, 300);

def getTheRows( db, exid, curid ):
    global utc_offset
    global how_far_back
    offset = 60 * 10 # 30 mins

    t = (time.time() - how_far_back )+ utc_offset
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
    pprint.pprint(rows)
    return rows


def runCalcs( args ):
    global params
    global exchange_id
    global currencypair_id
    global how_far_back

    if len(args) > 2:
        exchange_id = int( args[1] )
        currencypair_id = int( args[2])
        if len(args) > 3:
            how_far_back = int( args[3]) # SECONDS!!!

    db = None
    rows = None
    try:
        db = MySQLdb.connect(
            params["host"],
            params["user"],
            params["pass"],
            params["db"], 
            cursorclass=MySQLdb.cursors.DictCursor)
        rows = getTheRows( db, exchange_id, currencypair_id )
    except Exception, e:
        print "Failed to get mv avg: ", e
        db.rollback()
    finally:
        db.close()

    if rows != None:
        tenMins( db, exchange_id, currencypair_id, rows )
        thirtyMins( db, exchange_id, currencypair_id, rows )
        sixtyMins( db, exchange_id, currencypair_id, rows )
        twoFortyMins( db, exchange_id, currencypair_id, rows )
        sixHundyMins( db, exchange_id, currencypair_id, rows )
        oneDay( db, exchange_id, currencypair_id, rows )
        #twoDay( db, exchange_id, currencypair_id, rows )
        #fiveDay( db, exchange_id, currencypair_id, rows )
        #tenDay( db, exchange_id, currencypair_id, rows )

if __name__ == "__main__":
    runCalcs( sys.argv )
