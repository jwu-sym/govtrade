<strong>Project description: </strong>
The problem my project is aimed at solving is combating the distributed, unorganized information of government officials’ financial decisions. my project is for anyone who is interested in government officials’ financial disclosures and including their stocks and options transactions records. my project is unique because it identifies the ways in which political activities correlate with government officials’ financial transactions records. This enables transparency, eliminates the potential for insider trading, and identifies potential conflicts of interest. It allows retail investors to monitor and subsequently follow their trades before restrictions are made. 

<strong>Code Structure:</strong>

1. fetcher.py uses Python requests lib to fetch two main public sites.
  respectively: 
    - https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2024FD.zip all congress members' trades list disclosed in 2024.
    - https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2024/{docId} individual trade disclosure doc record.
    
    - fetcher.py attaches individual parsed trade doc to record
    - fetcher.py save records to postgresql database (hosted in Heroku)


2. processor.py helps fetcher.py convert raw data to structured records, extracts trades from trade pdf doc per record.
3. db.py inserts corresponding records to postgresql database hosted in heroku.
4. DB is postgresql, connection parameters are in .env file.
Sample db clip screenshot [here] https://govtrade-a46bca12cc9b.herokuapp.com/static/img/db_records.png

5. Run under project root directory:
    #### `python3 -m venv venv`
    #### `source ./venv/bin/activate`
    #### `pip install -r requirements.txt`
    #### `python src/fetcher.py`



