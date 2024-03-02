import os
import requests
import db
from zipfile import ZipFile
from processor import extract_trades, convert_record

from os import environ as env
from dotenv import load_dotenv
load_dotenv()

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
            lines = myfile.readlines()

    #columns = lines[0]
    
    records = []
    for line in lines[1:4]:
        
        record = convert_record(line)
        records.append(record)

        docId = record['docId']
        gtUrl = env['GOVTRADE_URL']
        url = f'{gtUrl}/{docId}.pdf'
        
        outfn = f'./data/{docId}.pdf' # trades file of the record
        resp = fetch(url, outfn)
        
        if resp:
            trades = extract_trades(outfn)
            record['trades'] = trades

        if not (record['trades']):
           continue

        if record['lastName'] == 'Pelosi':
            print(record)

        records.append(record)

    return records

def save_records(records):
    for record in records:
        db.insert_record(record)



if __name__ == '__main__' :
    url = 'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2024FD.zip'
    
    fn = env['GOVTRADE_FILE']  # congress members trades filename
    
    fetch(url, fn)

    records = process(fn)

    db.init()
    save_records(records)
