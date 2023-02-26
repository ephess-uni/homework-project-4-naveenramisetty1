# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    new_dates =[]
    for dts in old_dates:
        
        res = datetime.strptime(dts, "%Y-%m-%d").strftime('%d %b %Y')
        new_dates.append(res)
        
    return new_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        
        raise TypeError()
    
    set1 = []
    
    start_date = datetime.strptime(start, '%Y-%m-%d')
    
    for i in range(n):
        
        set1.append(start_date + timedelta(days=i))
        
    return set1


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    days1 = len(values)
    
    rangeslsit = date_range(start_date, days1)

   
    rqwet = list(zip(rangeslsit, values))
    return rqwet


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    output_data = defaultdict(float)
    hdrs_row = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".
              split(','))
    
    with open(infile, 'r') as f:
        completeLines = DictReader(f, fieldnames=hdrs_row)
        completerows = [row for row in completeLines]

    completerows.pop(0)
       
    for rw in completerows:
       
        patronID = rw['patron_id']
        
        date_due = datetime.strptime(rw['date_due'], "%m/%d/%Y")
        
        date_returned = datetime.strptime(rw['date_returned'], "%m/%d/%Y")
        
        daysoflate = (date_returned - date_due).days
        
        output_data[patronID]+= 0.25 * daysoflate if daysoflate > 0 else 0.0
        
                 
    finalHeades = [
        {'patron_id': p, 'late_fees': f'{f:0.2f}'} for p, f in output_data.items()
    ]
    outputHeader = ['patron_id', 'late_fees']
    with open(outfile, 'w') as f:
        
        writer = DictWriter(f,outputHeader)
        writer.writeheader()
        writer.writerows(finalHeades)


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
