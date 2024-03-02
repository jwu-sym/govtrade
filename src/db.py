from os import environ as env
from dotenv import load_dotenv

import psycopg2
from psycopg2 import DatabaseError
load_dotenv()

DATABASE_URL = env['DB_URL']

def execute(sql):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        conn.autocommit = True
        print(conn)
    except (Exception, DatabaseError) as error:
          print(error)  
          return

    with conn.cursor() as cur:
      try:
          cur.execute(sql)
      except (Exception, DatabaseError) as error:
          print(error)

    conn.close()

def init():
    fn = open(f'./src/schema/schema.sql', 'r')
    sql = fn.read()
    fn.close()

    execute(sql)

def insert_record(r):
    try:
        sql = "insert into trades (docId, firstName, lastName, filingType, stateDst, year, filingDate, trades) values('{}','{}','{}','{}','{}','{}','{}','{}')".format(
            r['docId'],
            r['firstName'], 
            r['lastName'],
            r['filingType'],
            r['stateDst'],
            r['year'],
            r['filingDate'],
            r['trades']
        )
        execute(sql)
    except (Exception, DatabaseError) as error:
        print(error)
    