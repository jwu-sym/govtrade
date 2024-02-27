#!/usr/bin/env python3

from flask import Flask, request
#from flask import send_from_directory


app = Flask(__name__,static_url_path='/static')

@app.route("/")
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
    if not len(input_text):
        input_text = 'Elena says Hi'
    return "You entered:" + input_text + '<br/> Have a nice day'



