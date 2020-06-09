import pygsheets
import requests
import json
import time
import os
import yagmail
from datetime import datetime
def joke():
    print("joke")
    URL = "https://icanhazdadjoke.com/"
    headers = {'Accept':'application/json'}
    r = requests.get(URL , headers = headers)
    json_joke = r.json()
    print(json_joke['joke'])
    return json_joke


def login_gsheet():
    print("login_gsheet")
    global worksheet
    try:
        gs = pygsheets.authorize(service_file = 'client_secret.json')
        #gs = pygsheets.authorize(service_account_env_var = os.environ.get('GDRIVE_API_CREDENTIALS'))
        sh = gs.open('Comment_ids')
        worksheet = sh.worksheets()[1]
        return worksheet
    except Exception as e:
        print(e)

def get_info():
    print("get_info")
    try:
        POST_ID_JOKE = (worksheet.get_col(1))
        EMAIL_ID = (worksheet.get_col(2))
        return (POST_ID_JOKE, EMAIL_ID)
    except Exception as e:
        print(e)

def update_info(POST_ID_JOKE,id):
    print("update_info")
    try:
        POST_ID_JOKE.append(id)
        worksheet.update_col(1,POST_ID_JOKE)
    except Exception as e:
        print(e)

def login():
    print("login_gmail")
    try:
        yag = yagmail.SMTP(user = "sample@123.com" , password ="Your password")
        return yag
    except Exception as e:
        print(e)

def send_mail(yag,json_joke):
    print("send_mail")
    try:
        for i in EMAIL_ID:
            yag.send( to=i , subject = ("Its dad joke time "+str(datetime.utcnow())) , contents = json_joke['joke'])
    except Exception as e:
        print(e)

def list_beautify(L1):
    print("list_beautify")
    try:
        l1 = list()
        for i in L1:
            if i != "":
                l1.append(i)
        return l1
    except Exception as e:
        print(e)

if __name__ == "__main__":
    try:
        while True:
            json_joke = joke()
            worksheet = login_gsheet()
            yag = login()
            POST_ID_JOKE , EMAIL_ID = get_info()
            POST_ID_JOKE = list_beautify(POST_ID_JOKE)
            EMAIL_ID = list_beautify(EMAIL_ID)
            send_mail(yag,json_joke)
            update_info(POST_ID_JOKE,json_joke['id'])
            time.sleep(3600)
    except:
        print("Error in main function!")
