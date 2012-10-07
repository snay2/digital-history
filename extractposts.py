import sqlite3
from datetime import datetime
import re
import calendar

#################################################
# Constants
#################################################
# Momento timestamps start at 1 January 2001 00:00:00
timestamp_origin = 978307200
# These work for my Momento database, but may differ for others
all_post_tags = ['note', 'facebook', 'twitter', '', 'lastfm', 'foursquare',
        'blogpost', '', 'instagram']


#################################################
# Inputs
#################################################
# Relative filename of the database
database_name = 'momento.db'
# Year of the posts to extract
process_year = 2012


#################################################
# Functions
#################################################

# Convert a timestamp to a string time with the given format
def convertTime(timestamp, format):
    timestamp += timestamp_origin
    return datetime.fromtimestamp(timestamp).strftime(format)

# Sanitize the text and escape any characters
def sanitizeText(text):
    if (text is None):
        return ''
    text = text.encode('ascii', 'ignore')
    text = re.sub(r'''([_#$&%])''', r'''\\\1''', text)
    return text

# Based on the integer post type, return a string for the post tag
def getPostTag(post_type):
    return all_post_tags[post_type]

# Loop over each result and output the correct LaTeX formatting
def outputPosts(rows):
    current_day = 0

    # Output the posts, grouped by day
    for row in rows:
        post_time = convertTime(row[1], "%H:%M")
        post_body = sanitizeText(row[2])
        post_tag = getPostTag(row[3])

        # Don't include empty posts or Twitter at-replies
        if (post_tag != '' and post_body[0] != '@'):
            # Output the day header if it hasn't already been done
            if (current_day != row[0]):
                post_date = convertTime(row[1], "%A %d %B %Y")
                print '\\subsection*{%s}\n' % (post_date)
                current_day = row[0]
            if (post_tag == 'instagram'):
                post_url = sanitizeText(row[4])
                print '\\%s{%s}{%s}{%s}\n' \
                        % (post_tag, post_time, post_body, post_url)
            elif (post_tag == 'blogpost'):
                post_url = sanitizeText(row[4])
                post_title = sanitizeText(row[5])
                print '\\%s{%s}{%s}{%s}\n' \
                        % (post_tag, post_time, post_title, post_url)
            else:
                print '\\%s{%s}{%s}\n' % (post_tag, post_time, post_body)

# Main function
def main(year):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    # Run the query for each month of the given year
    for month in range(1, 13):
        # Build the query
        query = 'select zday, zdate, zbody, zmomenttype, zurl, ztitle ' +\
            'from zmoment inner join zday ' +\
            'where zday.z_pk=zmoment.zday and zmoment.zbody!="" ' +\
            'and zday.zdatemonth=%s and zday.zdateyear=%s order by zdate asc;' \
            % (month, year)

        # Output chapter and section headings
        print '\\chapter*{%s}\n' % (calendar.month_name[month])
        print '\\section*{Background}\n'
        print '\\section*{Daily history}\n'

        # Output the posts for each day
        outputPosts(c.execute(query))

# Script main function handler
if __name__ == '__main__':
    main(process_year)

