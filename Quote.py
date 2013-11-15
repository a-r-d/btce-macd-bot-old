from sqlalchemy import create_engine, Column
from sqlalchemy import (Integer, Unicode, String, DateTime, Float)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
import time
import pprint
import datetime

Base = declarative_base()
ENGINE = None

def openDB():
    try:
        engine = create_engine("mysql+mysqldb://cryptotrends:crypto123lol@trollboxarchive.com/cryptotrends")
        print engine.execute("select 1").scalar()
        global ENGINE
        ENGINE = engine
        return engine
    except Exception, e:
        print "Exceptiion opening DB cxn: ", str(e)
        return None


def getSession():
    try:
        engine = None
        if ENGINE != None:
            engine = ENGINE
        else:
            engine = openDB()
        Session = sessionmaker()
        Session.configure( bind=engine )
        this_session = Session()
        if not this_session:
            raise Exception("Session was null")
        return this_session
    except Exception, e:
        print "Exceptiion getting a session: ", str(e)
        return None


class Quote(Base):
    __tablename__="quote"

    #keys
    id = Column(Integer,primary_key=True)
    exchange_id = Column(Integer)
    currencypair_id = Column(Integer)

    #meta data
    created = Column(DateTime)
    units = Column(String(10))

    #quote data
    last = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Float)
    average = Column(Float)
    bid = Column(Float)
    ask = Column(Float)

    #calculated quote data
    mv_avg_10_min = Column(Float)
    mv_avg_30_min = Column(Float)
    mv_avg_60_min = Column(Float)
    mv_avg_240_min = Column(Float)
    mv_avg_600_min = Column(Float)

    def __repr(self):
        return "quote: {0}, {1}, {2} id: {3}".format(self.created, self.last, self.units, self.id)


def getLast10Quote(session):
    res = session.query(Quote).order_by(Quote.created.desc()).limit(10);
    session.commit()
    return res


# note: db is in utc time, you are not I bet...
def getQuotesNewerThanSeconds( session, utc_offset, timeperiod ):
    t = (time.time() - timeperiod) + utc_offset
    filterdate = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
    res = session.query(Quote).filter(
        Quote.created > filterdate )
    session.commit()
    return res

# note: db is in utc time, you are not I bet...
def getQuotesNewerThanSecondsCurrEx( session, utc_offset, timeperiod, currencypair_id, exchange_id):
    t = (time.time() - timeperiod) + utc_offset
    filterdate = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
    res = session.query(Quote).filter(
        and_( 
            Quote.created > filterdate,
            Quote.currencypair_id==currencypair_id,
            Quote.exchange_id==exchange_id   
        ))
    session.commit()
    return res

def test():
    session = getSession()
    if not session:
        raise Exception("Session is null!!!!")

    # test 10 latest:
    print "test last 10 quotes" * 3
    res = getLast10Quote(session)
    for r in res:
        print r.last, r.created, r.units

    # test 1 hour quotes:
    print "test last half hour" * 3
    utc_5 = 60 * 60 * 5
    res = getQuotesNewerThanSeconds(session, utc_5, 60 * 30 )
    for r in res:
        print r.last, r.created, r.units

    # test 1 hour quotes:
    print "test last hour - USD/LTC" * 3
    utc_5 = 60 * 60 * 5
    res = getQuotesNewerThanSecondsCurrEx(session, utc_5, 60 * 60, 1, 1 )
    for r in res:
        print r.last, r.created, r.units


if __name__ == '__main__':
    test()







