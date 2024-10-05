import requests
from zipfile import ZipFile


import sys
sys.path.append('src')

import os
import argparse
import db
from processor import extract_trades, convert_record
from service import read_records

from os import environ as env
from dotenv import load_dotenv
load_dotenv()

def fetch(url, filename):
    response = requests.get(url)
    
    if response.status_code == 404:
        print(f'skipped: {url} ')
        return None
    
    content = response.content
    if not content:
        print('error')
        return None

    print(f'fetching {url}')

    f = open(filename, 'wb')
    f.write(content)
    f.close()

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
        db.insert_record(record)

def fetch_historical(years=['2023']):#,'2022','2021'
    for year in years:
        main(year)

#@scheduler.task('cron', id='do_job_3', week='*', day_of_week='sun')
def update(year='2024'):
    print('start update job')

    base_url = env['GOVTRADELIST_URL']
    url = f'{base_url}/{year}FD.zip'
    fn = f'/tmp/{year}FD.zip' # congress members trades filename
    fetch(url, fn) # fetch gov trades list

    records = parse(fn, year)
    existing_recs = read_records(year)
    
    docIds = [row['docId'] for row in existing_recs]

    print(f'# of existing records {len(existing_recs)} {len(docIds)} new fetched {len(records)}')
    
    new_records = []
    
    for record in records:
        if record['docId'] not in docIds:
            new_records.append(record)
    
    #new_records = existing_recs[0:2]
    
    if len(new_records):
        fetch_trade_docs(new_records)
        save_records(new_records)
        print(f'Inserted #{len(new_records)} new records ')
    
    new_records = existing_recs[0:1000]
    
    #new_records = [rec for rec in new_records if rec["firstName"] == 'Nancy']
    
    return new_records

#@scheduler.task('cron', id='do_job_3', week='*', day_of_week='sun')
def main(year='2024'):
    
    fn = f'/tmp/{year}FD.zip' # congress members trades filename
    base_url = env['GOVTRADELIST_URL']
    url = f'{base_url}/{year}FD.zip'
    
    fetch(url, fn) # fetch gov trades list

    records = parse(fn, year)
    fetch_trade_docs(records) # fetch individual trade doc per record
    os.remove(fn)

    #db operations # init()
    db.remove_records(f"year='{year}'")
    save_records(records)
    db.close()

    print('Job  executed')

def remove_record(id):
    db.remove_records(f"id={id}")

    
    
if __name__ == '__main__' :
    parser = argparse.ArgumentParser(prog='GovTrade Fetcher', description='Fetching Government Financial Records')
    parser.add_argument("--main", help="main fetcher")
    parser.add_argument("--update", help="incremental fetcher")
    parser.add_argument("--historical", help="fetch historicals")
    parser.add_argument("--remove", help="remove records")
    parser.add_argument("--init", help="remove schema")
    
    
    args = parser.parse_args()
    
    
    if args.main:
        main()
    elif args.update:
        update()
    elif args.historical:
        fetch_historical()
    elif args.init:
        db.init()
    elif args.remove:
        id = args.remove
        remove_record(id)
    
