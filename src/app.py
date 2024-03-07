#!/usr/bin/env python3
import sys
sys.path.append('src')

from flask import Flask, request, render_template
#from flask import send_from_directory

#import time
import atexit
from service import get_records, get_lastrun, set_lastrun

from apscheduler.schedulers.background import BackgroundScheduler
                
app = Flask(__name__,static_url_path='/static')


@app.route("/echo")
def main():
    return '''
     <form action="/echo_input" method="POST">
         <input name="user_input">
         <input type="submit" value="Submit!">
     </form>
     <img width="200" src="/static/img/elena.png"></img>

     '''

@app.route("/echo_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input", "")
    return "You entered:" + input_text + '<br/> Have a nice day'


@app.route("/", methods=["GET"])
def records():
    year = request.args.get("year", '2024')
    records = get_records(year)
    print(f'# of records {len(records)}')
    lastrun = get_lastrun()
    return render_template('index.html', records=records, year=year, lastrun=lastrun)
   

def app_init():
    set_lastrun()
    start_job_scheduler()

def fetch_job():
    from fetcher import main
    main()
    set_lastrun()

def update_job():
    from fetcher import update
    update()
    set_lastrun()

def start_job_scheduler():
    scheduler = BackgroundScheduler()    
    scheduler.add_job(func=update_job, trigger="interval", seconds=7200)
    scheduler.add_job(func=fetch_job, trigger="interval", seconds=86400)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


app_init()


