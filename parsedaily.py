import sqlite3
from datetime import datetime
from datetime import timedelta
from dateutil import tz
import re

timestamp_origin = 978307200 # 1 January 2001 00:00:00 GMT

# Convert a UTC timestamp to local timezone
def convertTime(timestamp):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utcstamp = timestamp + timestamp_origin
    utcdate = datetime.fromtimestamp(utcstamp)
    utcdate = utcdate.replace(tzinfo=from_zone)
    localdate = utcdate.astimezone(to_zone)
    # This conversion is off by -6 hours. Not sure why.
    return localdate + timedelta(hours=6)

# Sanitize the body and escape any characters
def sanitizeText(body):
    body = body.encode('ascii', 'ignore')
    modified = re.sub(r'''([_#$&%])''', r'''\\\1''', body)
    return modified

conn = sqlite3.connect('momento.db')
c = conn.cursor()

# Run the query
query = 'select zday, zdate, zbody from zmoment inner join zday where ' +\
    'zday.z_pk=zmoment.zday and zmoment.zmomenttype=2 order by zdate asc;'

daytracker = 0

# Output the posts, grouped by day
for row in c.execute(query):
    thisdate = convertTime(row[1]).strftime("%A %d %B %Y")
    thistime = convertTime(row[1]).strftime("%H:%M")
    thisbody = sanitizeText(row[2])
    if (thisbody[0] != '@'):
        if (daytracker != row[0]):
            print '\\subsection*{%s}\n' % (thisdate)
            daytracker = row[0]
        print '\\twitter{%s}{%s}\n' % (thistime, thisbody)

