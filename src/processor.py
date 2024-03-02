from PyPDF2 import PdfReader 
import db

def convert_record(line):
    line = str(line)
        
    line = line[1:]

    line = line.replace('\\r\\n', '')
    line = line.replace('\'', '')
    line = line.split('\\t')

    o = {'firstName':'',
         'lastName':'',
         'filingType':'',
         'stateDst':'',
         'year':'',
         'filingDate':'',
         'docId':'',
         'trades':''}

    
    o['lastName'] = line[1]
    o['firstName'] = line[2]

    o['filingType'] = line[4]
    o['stateDst'] = line[5]
    o['year'] = line[6]
    o['filingDate'] = line[7]
    o['docId'] = line[8]

    return o


def extract_trades(fn):
    # creating a pdf reader object 
    reader = None
    try:
        reader = PdfReader(fn) 
    except:
        pass
    
    if not reader or len(reader.pages) < 1:
        return None
    
    page = reader.pages[0]
    
    
    text = page.extract_text() 
    text = text.replace('\x00','')
    text = text.replace('\'','')

    trades = text
    try:
        text = text.split('ID')[1]
        text = text.split('Gains >\n$200?\n')[1]
        trades = text.split('* For the complete')[0]
        trades = '|'.join(trades.split('F S:'))

    except Exception as e:
        print(f'Error processing {fn}')
    
    return trades


def get_records():
    
    columns = ['id', 'docId', 'firstName', 'lastName', 'filingType', 'stateDst', 'year', 'filingDate', 'trades']
    rows = db.read_records(columns)

    records = []
    for row in rows:
        r = {}
        for i in range(len(columns)):    
            r[columns[i]] = row[i]
        
        if not len(r['trades']):
            continue
        
        records.append(r)
    return records

