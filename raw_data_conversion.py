import re
import csv

# Raw data that is being used - replace with your data or updated data (example below)
raw_data = """
Workday, Inc. 	NASDAQ:WDAY 	12/02/24 	Buy 		$299.09 	$291.92 	-2.4% 	0.8% 	-3.2%
"""
# Adjusted pattern to accommodate your provided data structure
pattern = re.compile(
    r'(?P<company>.+?)\s+'
    r'(?P<exchange>LSE:|NYSE:|NASDAQ:)(?P<code>\w+)\s+'
    r'(?P<rec_date>\d{2}/\d{2}/\d{2})\s+'
    r'(?P<rec_status>Buy|Hold|Sold|Buy/Starter|BestBuyNow)\s+'
    r'(?:\d{2}/\d{2}/\d{2}\s+)?'  # Optional close date
    r'(?P<cost>\$?\d+(?:\.\d+)?)\s+'
    r'(?P<recent_close>\$?\d+(?:\.\d+)?)\s+'
    r'(?P<return>[\-]?\d+\.\d+)%\s+'
    r'(?P<sp_uk>[\-]?\d+\.\d+)%\s+'
    r'(?P<vs_sp_uk>[\-]?\d+\.\d+)%'
)
# Open the output CSV
with open('stocks_data.csv', 'w', newline='') as outfile:
    csv_writer = csv.writer(outfile)
    # Write the headers
    headers = ['Company', 'Exchange', 'Rec Date', 'Rec Status', 'Cost', 'Recent Close', 'Return', 'S&P UK',
               'Vs S&P UK']
    csv_writer.writerow(headers)

    # Process each line in the raw_data string
    for line in raw_data.strip().split("\n"):
        match = pattern.match(line)
        if match:
            # Extract data for each matched line
            data = match.groupdict()
            row = [
                data['company'], data['exchange'], data['rec_date'],
                data['rec_status'], data['cost'], data['recent_close'],
                data['return'], data['sp_uk'], data['vs_sp_uk']
            ]
            csv_writer.writerow(row)

print("Conversion complete. Data saved to stocks_data.csv.")
