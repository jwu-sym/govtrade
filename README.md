<strong>Project description: </strong>
The problem my product is aimed at solving is combating the distributed, unorganized information of government officials’ financial decisions. My product is for anyone who is interested in government officials’ financial disclosures and including their stocks and options transactions records. My product is unique because it identifies the ways in which political activities correlate with government officials’ financial transactions records. This enables transparency, eliminates the potential for insider trading, and identifies potential conflicts of interest. It allows retail investors to monitor and subsequently follow their trades before restrictions are made. 

Code Structure:

1. fetcher.py uses requests lib to fetch two main public sites.
  respectively: a. https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2024FD.zip all congress members' trading records in 2024.
  b.  many trades files on https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2024/{docId} where docId is the value from above acquired file

3. processor.py converts downloaded raw data to structured records and extracts trades from second files per each congress member.
4. db.py inserts corresponding records to postgresql database hosted in heroku.

5. Run under project root directory:
 #### `python3 -m venv venv`
 #### `source ./venv/bin/activate`
 #### `pip install -r requirements.txt`
 #### `python src/fetcher.py `



