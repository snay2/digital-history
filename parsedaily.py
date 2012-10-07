import sqlite3
from datetime import datetime
from datetime import timedelta
from dateutil import tz
import re
import calendar

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
    body = re.sub(r'''([_#$&%])''', r'''\\\1''', body)
    return body

all_post_types = ['note', 'facebook', 'twitter', '', 'lastfm', 'foursquare',
        'blogpost', '', 'instagram']

def getPostTag(index):
    # Don't include last.fm or foursquare posts
    if (index in [4, 5]):
        return ''
    return all_post_types[index]

def outputPosts(rows):
    current_day = 0

    # Output the posts, grouped by day
    for row in rows:
        post_time = convertTime(row[1]).strftime("%H:%M")
        post_body = sanitizeText(row[2])
        post_tag = getPostTag(row[3])

        if (post_tag != '' and post_body[0] != '@'):
            # Output the day header if it hasn't already been done
            if (current_day != row[0]):
                post_date = convertTime(row[1]).strftime("%A %d %B %Y")
                print '\\subsection*{%s}\n' % (post_date)
                current_day = row[0]
            print '\\%s{%s}{%s}\n' % (post_tag, post_time, post_body)

def main(year):
    conn = sqlite3.connect('momento.db')
    c = conn.cursor()

    # Run the query for each month of the given year
    for month in range(1,13):
        query = 'select zday, zdate, zbody, zmomenttype from zmoment ' +\
            'inner join zday ' +\
            'where zday.z_pk=zmoment.zday and zmoment.zbody!="" ' +\
            'and zday.zdatemonth=%s and zday.zdateyear=%s order by zdate asc;' \
            % (month, year)

        print '\\chapter*{%s}\n' % (calendar.month_name[month])
        print '\\section*{Background}\n'
        print '\\section*{Daily history}\n'
        outputPosts(c.execute(query))

if __name__ == '__main__':
    main(2012)

