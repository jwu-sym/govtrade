from db import read_records

def get_records(year='2024'):
    columns = ['id', 'docId', 'firstName', 'lastName', 'filingType', 'stateDst', 'year', 'filingDate', 'trades']
    rows = read_records(columns, filter=f"year='{year}'")

    records = []
    for row in rows:
        r = {}
        for i in range(len(columns)):    
            r[columns[i]] = row[i]
        
        if not len(r['trades']):
            continue

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

        #if r['lastName'] in ['Pelosi']:
        #    print(f'{r["lastName"]} {len(trades)} {trades}')
        

        records.append(r)
    return records

def get_last_run():
    last_run = None
    try:
        f = open('/tmp/gt_lastrun')
        last_run = f'{str(f.read())[:19]}'
        f.close()
    except:
        pass
    return last_run