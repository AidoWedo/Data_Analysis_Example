import streamlit as st
import pandas as pd
import re
import csv
from io import StringIO, BytesIO  # Import BytesIO


# Function to convert raw data to CSV
def convert_to_csv(raw_data):
    pattern = re.compile(
        r'(?P<company>.+?)\s+'
        r'(?P<exchange>LSE:|NYSE:|NASDAQ:)(?P<code>\w+)\s+'
        r'(?P<rec_date>\d{2}/\d{2}/\d{2})\s+'
        r'(?P<rec_status>Buy|Hold|Sold)\s+'
        r'(?:\d{2}/\d{2}/\d{2}\s+)?'  # Optional close date
        r'(?P<cost>\$?\d+(?:\.\d+)?)\s+'
        r'(?P<recent_close>\$?\d+(?:\.\d+)?)\s+'
        r'(?P<return>[\-]?\d+\.\d+)%\s+'
        r'(?P<sp_uk>[\-]?\d+\.\d+)%\s+'
        r'(?P<vs_sp_uk>[\-]?\d+\.\d+)%'
    )

    output = StringIO()
    csv_writer = csv.writer(output)

    headers = ['Company', 'Exchange', 'Code', 'Rec Date', 'Rec Status', 'Cost', 'Recent Close', 'Return', 'S&P UK',
               'Vs S&P UK']
    csv_writer.writerow(headers)

    for line in raw_data.strip().split("\n"):
        match = pattern.match(line)
        if match:
            data = match.groupdict()
            row = [
                data['company'], data['exchange'] + data['code'], data['rec_date'],
                data['rec_status'], data['cost'], data['recent_close'],
                data['return'], data['sp_uk'], data['vs_sp_uk']
            ]
            csv_writer.writerow(row)

    output.seek(0)  # Go to the start of the StringIO object
    # Convert StringIO to BytesIO for binary data format
    return BytesIO(output.getvalue().encode())


# Streamlit UI
st.title('Data to CSV Converter')

# Text area for user to paste data
raw_data = st.text_area("Paste your data here:", height=300)

if st.button('Convert to CSV'):
    if raw_data:
        # Convert the data to CSV
        csv_output = convert_to_csv(raw_data)
        # Create a link for downloading
        st.download_button(label="Download CSV", data=csv_output, file_name="converted_data.csv", mime='text/csv')
    else:
        st.write("Please paste some data into the text area above.")