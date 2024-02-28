import os
import requests
from zipfile import ZipFile
from processor import extract_trades, convert_record

def fetch(url, filename):
    response = requests.get(url)
    
    if response.status_code == 404:
        #print(f'skipped: {url} ')
        return None
    
    content = response.content
    if not content:
        return None

    print(f'fetching {url}')

    f = open(filename, 'wb')
    f.write(content)

    return content

def process(filename):
    lines = None

    with ZipFile(filename) as myzip:
        with myzip.open('2024FD.txt') as myfile:
            lines = (myfile.readlines())

    #columns = lines[0]
    
    #result = []
    docIds = []
    
    records = []
    for line in lines[1:]:
        
        record = convert_record(line)
        records.append(record)

        docId = record['docId']
        url = f'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2024/{docId}.pdf'
        
        dir = get_data_dir()
        pdf = f'{dir}/{docId}.pdf' # trades file for the record
        resp = fetch(url, pdf)
        if resp:
            trades = extract_trades(pdf)
            record['trades'] = trades

        #result.append(line)
    
    print(records)
    

def get_data_dir():
    dir = os.getcwd()
    dir = dir.replace('/src','')  # ensure data output directory under project root
    
    return f'{dir}/data'


if __name__ == '__main__' :
    url = 'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2024FD.zip'
    
    dir = get_data_dir()
    
    fn = f'{dir}/2024FD.zip'
    
    fetch(url, fn)

    process(fn)
