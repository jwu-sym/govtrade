import os
import requests
from zipfile import ZipFile

def fetch(url, filename):
    response = requests.get(url)
    
    if response.status_code == 404:
        #print(f'skipped: {url} ')
        return

    
    f = open(filename, 'wb')
    f.write(response.content)

def process(filename):
    lines = None

    with ZipFile(filename) as myzip:
        with myzip.open('2024FD.txt') as myfile:
            lines = (myfile.readlines())

    columns = lines[0]
    
    result = []
    docIds = []
    
    for line in lines[1:]:
        line = str(line)
        
        line = line[1:]

        line = line.replace('\\r\\n', '')
        line = line.replace('\'', '')
        line = line.split('\\t')

        #if line[1] !='Pelosi':
        #    continue

        docId = line[-1]
        docIds.append(docId)

        url = f'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2024/{docId}.pdf'

        dir = get_data_dir()
        
        fetch(url, f'{dir}/data/{docId}.pdf')
        
        result.append(line)
    
    print(result[0])
    print(result[1:2])
    
    #'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2024/'
    #print(docIds)

def get_data_dir():
    dir = os.getcwd()
    dir = dir.replace('/src','')  # ensure data output directory under root

    return dir

if __name__ == '__main__' :
    url = 'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2024FD.zip'
    
    dir = get_data_dir()
    
    fn = f'{dir}/data/2024FD.zip'
    
    fetch(url, fn)

    process(fn)
