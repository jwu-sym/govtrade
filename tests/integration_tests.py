import unittest

import sys
sys.path.append('src')

from service import get_records, get_lastrun
from fetcher import *

class TestSum(unittest.TestCase):

    def test_get_records(self):
        records = get_records()
        num = len(records)
        self.assertGreater(num, 0, "Records should be greater than 0")

    def test_get_lastrun(self):
        lastrun = get_lastrun()
        if lastrun:
            num = len(lastrun)
            self.assertEqual(num, 19, "Records last run timestamp should not be empty")

    def test_parse_records(self):
        
        fn = 'data/2024FD.zip' # congress members trades filename
        records = parse(fn)
        num = len(records)
        self.assertGreater(num, 0, "# of Records parsed should be greter 0")
    

    def test_record(self):
        records = get_records()
        record = records[0]
        self.assertIsNotNone(record['lastName'], "Record should have last name")
        self.assertIsNotNone(record['firstName'], "Record should have first name")
        self.assertIsNotNone(record['filingDate'], "Record should have filing date")
        self.assertIsNotNone(record['stateDst'], "Record should have state District")
        self.assertIsNotNone(record['filingType'], "Record should have filing type")
        self.assertIsNotNone(record['docId'], "Record should have docId")
        

    def test_record_trades(self):
        records = get_records()
        record = records[1]
        self.assertGreater(len(record['trades']), 0, "Record should have trades")
    
        desc = record['desc']
        self.assertTrue('Buy' in desc or 'Sell' in desc, "Record should have trade type")

if __name__ == '__main__':
    unittest.main()
