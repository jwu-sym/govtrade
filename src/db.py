from os import environ as env
from dotenv import load_dotenv

import psycopg2

load_dotenv()
print(env['DB_URL'])


DATABASE_URL = env['DB_URL']

def execute(sql):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    conn.autocommit = True
    print(conn)

    with conn.cursor() as cur:
      try:
          cur.execute(sql)
      except (Exception, psycopg2.DatabaseError) as error:
          print(error)

    conn.close()

def init():
    fn = open(f'./src/schema/schema.sql', 'r')
    sql = fn.read()
    fn.close()

    execute(sql)

def insert_record(r):
    sql = "insert into trades values('{}','{}','{}','{}','{}','{}','{}','{}')".format(
        r['firstName'], 
        r['lastName'],
        r['filingType'],
        r['stateDst'],
        r['year'],
        r['filingDate'],
        r['docId'],
        r['trades']
    )
    execute(sql)
    