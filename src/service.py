from .db import read_records

def get_records():
    
    columns = ['id', 'docId', 'firstName', 'lastName', 'filingType', 'stateDst', 'year', 'filingDate', 'trades']
    rows = read_records(columns)

    records = []
    for row in rows:
        r = {}
        for i in range(len(columns)):    
            r[columns[i]] = row[i]
        
        if not len(r['trades']):
            continue
        if r['lastName'] == 'Pelosi':
            print(r['trades'])
            
        records.append(r)
    return records

