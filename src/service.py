import db
import re
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
        trade_data = ''
        
        action = ''
        amount = ''
        trade_date = ''
        symbol = ''
        last_line = ''
        for trade in r['trades'].split('|'):
            if '[ST]' in trade:
                last_line = str(trade)

                tmp_start = trade.index('[ST]') + 4
                tmp = trade[tmp_start:].strip()
                action = tmp[0] == 'S' and 'Sell' or 'Buy'

                trade_data = tmp
                
                trade_date_tmp = trade_data.split(' ')[-5:-4]
                trade_date = ''.join(trade_date_tmp)

                amt_tmp = trade_data.split(' ')[-3:]
                amount = ' '.join(amt_tmp)

                regex = r"\((.*?)\)"
                symbol = re.search(regex, last_line).group(1)
                

            if '[GS]' in trade:
                last_line = str(trade)

                tmp_start = trade.index('[GS]') + 4
                tmp = trade[tmp_start:].strip()
                action = tmp[0] == 'S' and 'Sell' or 'Buy'

                trade_data = tmp
                
                trade_date_tmp = trade_data.split(' ')[-5:-4]
                trade_date = ''.join(trade_date_tmp)

                amt_tmp = trade_data.split(' ')[-3:]
                amount = ' '.join(amt_tmp)

                symbol = last_line.split('[GS]')[0]


            trade = trade.replace('\n', '<br/>')

            trade = trade.replace('] S ', ']S ')
            trade = trade.replace('] P ', ']P ')

            trade = trade.replace(']S ', ']Sell ')
            trade = trade.replace(']P ', ']Buy ')
            
            trade = trade.replace('[ST]', '<br/><b>Stock: </b>')
            trade = trade.replace('[OP]', '<br/><b>Option: </b>')
            trade = trade.replace('[GS]', '<br/><b>Bond: </b>')
            trade = trade.replace('[PS]', '<br/><b>Private Equity: </b>')
            trade = trade.replace('[CS]', '<br/><b>Convertible Note: </b>')
            trade = trade.replace('[OT]', '<br/><b>Crypto: </b>')

            trade = trade.replace('(', '(<b>')
            trade = trade.replace(')', '</b>)')

            trades.append(trade)
            
            

        r['desc'] = ' '.join(trades)
        r['trades'] = trade_data #' '.join(trade_data)
        r['action'] = action
        r['amount'] = amount
        r['symbol'] = symbol
        r['tradeDate'] = convert_shortform_us_date_to_date(trade_date)
    return records

def set_lastrun():
    f = open('/tmp/gt_lastrun.ts','w')
    f.write(f'{datetime.now()}')
    f.close()

def get_lastrun():
    last_run = None
    try:
        f = open('/tmp/gt_lastrun.ts')
        last_run = f'{str(f.read())[:19]}'
        f.close()
    except:
        pass
    return last_run

import datetime

def convert_shortform_us_date_to_date(date_string):
    if '/' not in date_string:
        return date_string
    month, day, year = date_string.split("/")
    # Create a date object from the components.
    date = datetime.date(int(year), int(month), int(day))

    return date.strftime('%Y-%m-%d')
