import requests
from zipfile import ZipFile
from datetime import datetime

import sys
sys.path.append('src')

from db import *
from processor import extract_trades, convert_record
from os import remove
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

def parse(filename, year='2024'):
    lines = None

    with ZipFile(filename) as myzip:
        csvfile = f'{year}FD.txt'
        with myzip.open(csvfile) as myfile:
            lines = myfile.readlines()

    #columns = lines[0]
    
    records = []
    for line in lines[1:]:
        
        record = convert_record(line)
        records.append(record)

    print(f'Parsed # of records {len(records)}')

    return records

    

def fetch_trade_docs(records):
    base_url = env['GOVTRADE_URL']
    
    for record in records:
        docId = record['docId']
        year = record['year']
        url = f'{base_url}/{year}/{docId}.pdf'
    
        outfn = f'/tmp/{docId}.pdf' # trades file of the record
        content = fetch(url, outfn)
        
        trades = None
        if content:
            trades = extract_trades(outfn)
        
        if not trades:
            trades = ''
        
        record['trades'] = trades
        
        if record['lastName'] == 'Pelosi':
            print(record)


def save_records(records):
    #print(f'saving # records {len(records)}')
    for record in records:
        insert_record(record)

def fetch_historical(years=['2023','2022','2021']):
    for year in years:
        main(year)

#@scheduler.task('cron', id='do_job_3', week='*', day_of_week='sun')
def main(year='2024'):
    
    fn = f'{year}FD.zip' # congress members trades filename
    base_url = env['GOVTRADELIST_URL']
    url = f'{base_url}/{fn}'
    
    fetch(url, fn) # fetch gov trades list

    records = parse(fn, year)
    fetch_trade_docs(records) # fetch individual trade doc per record
    remove(fn)

    #db operations # init()
    remove_records(f"year='{year}'")
    save_records(records)
    close()

    f = open('/tmp/gt_lastrun','w')
    f.write(f'{datetime.now()}')
    f.close()

    print('Job  executed')

if __name__ == '__main__' :
    main()
    #fetch_historical()
    
