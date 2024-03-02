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

def parse(filename):
    lines = None

    with ZipFile(filename) as myzip:
        with myzip.open('2024FD.txt') as myfile:
            lines = myfile.readlines()

    #columns = lines[0]
    
    records = []
    for line in lines[1:]:
        
        record = convert_record(line)
        records.append(record)

    print(f'Parsed # of records {len(records)}')

    return records

def fetch_trade_doc(docId):
    gtUrl = env['GOVTRADE_URL']
    url = f'{gtUrl}/{docId}.pdf'
    
    outfn = f'./data/{docId}.pdf' # trades file of the record
    resp = fetch(url, outfn)
    #resp = True
    
    if resp:
        trades = extract_trades(outfn)
        return trades

def fetch_trades(records):

    for record in records:
        docId = record['docId']
        trades = fetch_trade_doc(docId) # fetch individual trade doc

        record['trades'] = trades
        
        if record['lastName'] == 'Pelosi':
            print(record)


def save_records(records):
    for record in records:
        db.insert_record(record)

#@scheduler.task('cron', id='do_job_3', week='*', day_of_week='sun')
def main():
    url = env['GOVTRADELIST_URL']
    fn = env['GOVTRADE_FILE']  # congress members trades filename
    
    fetch(url, fn) # fetch gov trades list

    records = parse(fn)
    fetch_trades(records) # fetch individual trade doc per record

    db.init()
    save_records(records)
    db.close()

    print('Job  executed')

if __name__ == '__main__' :
    main()
