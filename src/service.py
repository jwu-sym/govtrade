import db
from datetime import datetime

def read_records(year='2024'):
    columns = ['id', 'docId', 'firstName', 'lastName', 'filingType', 'stateDst', 'year', 'filingDate', 'trades']
    rows = db.read_records(columns, filter=f"year='{year}'", orderBy='filingDate')
    records = []
    for row in rows:
        r = {}
        for i in range(len(columns)):    
            r[columns[i]] = row[i]
        records.append(r)

    return records

def get_records(year='2024'):
    
    records = read_records(year)

    records = [r for r in records if len(r['trades'])]
            
    convert_trades(records)

    return records


def convert_trades(records):
    for r in records:
        
        trades = []
        for trade in r['trades'].split('|'):
            trade = trade.replace('\n', '<br/>')

            trade = trade.replace(']S ', ']Sell ')
            trade = trade.replace(']P ', ']Buy ')
            trade = trade.replace('] S ', ']Sell ')
            trade = trade.replace('] P ', ']Buy ')

            trade = trade.replace('[ST]', '<br/><b>Stock: </b>')
            trade = trade.replace('[OP]', '<br/><b>Option: </b>')
            trade = trade.replace('[GS]', '<br/><b>Bond: </b>')
            trade = trade.replace('[PS]', '<br/><b>Private Equity: </b>')
            trade = trade.replace('[CS]', '<br/><b>Convertible Note: </b>')
            trade = trade.replace('[OT]', '<br/><b>Crypto: </b>')

            trade = trade.replace('(', '(<b>')
            trade = trade.replace(')', '</b>)')

            trades.append(trade)
        
        r['trades'] = ' '.join(trades)
    return records

def set_lastrun():
    f = open('./tmp/gt_lastrun','w')
    f.write(f'{datetime.now()}')
    f.close()

def get_lastrun():
    last_run = None
    try:
        f = open('./tmp/gt_lastrun')
        last_run = f'{str(f.read())[:19]}'
        f.close()
    except:
        pass
    return last_run

