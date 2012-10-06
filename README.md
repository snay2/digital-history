# digital-history

I use an iPhone app called [Momento][http://www.momentoapp.com/]  to archive my tweets, Facebook posts, Instagram pictures, blog posts, and personal diary notes. I want a way to compile all of that personal digital history into a format that can be preserved for my posterity like my physical written journals are.

This project takes the Momento backup database (which can be exported via the app settings) and creates a nicely-formatted LaTeX document that can then be printed.

I am starting with recognizing the formats I use but may extend it to all the data types Momento allows.

## Running digital-history

Follow these steps to use digital-history:

1. In Momento, go to Settings -> Data -> Backup & Restore -> Create New Backup
1. In iTunes, find the backup file created by Momento and copy it to your computer
1. Rename the file from `*.momento` to `*.zip`.
1. Unzip the file. Find the Database.momentodb file.
1. Copy that into the same directory as the Python script in this project
1. Rename it to `momento.db`
1. At the command line, run `python parsedaily.py > out.tex`

The output of the script is a partial LaTeX file that can be included with `\input`.

