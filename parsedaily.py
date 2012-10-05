import sqlite3
from datetime import datetime
from dateutil import tz

timestamp_origin = 978307200 # 1 January 2001 00:00:00 GMT

def convertTime(timestamp):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utcstamp = timestamp + timestamp_origin
    print utcstamp
    utcdate = datetime.fromtimestamp(utcstamp)
    utcdate = utcdate.replace(tzinfo=from_zone)
    # This conversion is off by -5 hours. Not sure why.
    localdate = utcdate.astimezone(to_zone)
    return localdate

conn = sqlite3.connect('momento.db')
c = conn.cursor()

query = 'select zdate, zbody from zmoment inner join zday where ' +\
    'zday.z_pk=zmoment.zday and zmoment.zmomenttype=2 order by zdate asc;'

for row in c.execute(query):
    thisdate = convertTime(row[0])
    thisbody = row[1]
    print thisdate, thisbody.encode('ascii', 'ignore')

