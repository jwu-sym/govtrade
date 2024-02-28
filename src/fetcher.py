import os
import requests
from zipfile import ZipFile

def fetch(url, filename):
    response = requests.get(url)
    
    if response.status_code == 404:
        #print(f'skipped: {url} ')
        return

    print(f'fetching{url}')

    f = open(filename, 'wb')
    f.write(response.content)

def process(filename):
    lines = None

    with ZipFile(filename) as myzip:
        with myzip.open('2024FD.txt') as myfile:
            lines = (myfile.readlines())

    columns = lines[0]
    
    #result = []
    docIds = []
    
    records = []
    for line in lines[1:]:
        
        record = convert_record(line)
        records.append(record)

        #if line[1] !='Pelosi':
        #    continue

        docId = record['docId']
        url = f'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2024/{docId}.pdf'
        
        dir = get_data_dir()
        
        fetch(url, f'{dir}/data/{docId}.pdf')
        
        #result.append(line)
    
    print(records[-1])
    
    
    #'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2024/'
    #print(docIds)

def get_data_dir():
    dir = os.getcwd()
    dir = dir.replace('/src','')  # ensure data output directory under root

    return dir


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
         'docId':''
         }

    o['firstName'] = line[2]
    o['lastName'] = line[1]
    o['docId'] = line[8]


    return o

if __name__ == '__main__' :
    url = 'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2024FD.zip'
    
    dir = get_data_dir()
    
    fn = f'{dir}/data/2024FD.zip'
    
    fetch(url, fn)

    process(fn)
