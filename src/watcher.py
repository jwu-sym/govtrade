import sys
sys.path.append('src')

from os import environ as env
from dotenv import load_dotenv
load_dotenv()

import mailtrap as mt

def send_mail(recs):
    html = render_text(recs)
    mail = mt.Mail(
        sender = mt.Address(email=f"{env['MAIL_SENDER']}"),
        to = [mt.Address(email=f"{env['MAIL_RECIPIENT']}")],
        subject = "GovTrade: New trades by Members of Congress!",
        html = html
        
    )

    client = mt.MailtrapClient(token=f"{env['MAIL_TOKEN']}")
    client.send(mail)
    print('sent mail %s %s' % (html, env['MAIL_RECIPIENT']))


def render_text(recs):
    texts = []
    for r in recs:
        try:
            text = f"<b> {r['firstName']} {r['lastName']} </b>disclosed new trade on {r['filingDate']}:"
            text += f"<br/> <small> {r['trades']} </small>"
            texts.append(text)
        except:
            pass

    return '<br/>'.join(texts)


