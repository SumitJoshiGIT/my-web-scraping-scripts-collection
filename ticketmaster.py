from flask import (flash, Flask, redirect, render_template, request,
                   session, url_for, send_file, jsonify)
from aiohttp import ClientSession,BasicAuth                                                                                                                                                                                                  
import asyncio 
from werkzeug.utils import secure_filename
import os
import time
import json
import pandas as pd

from random import choice

UA=[
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0"
]


IPROYAL_USER = os.environ.get('IPROYAL_USER')
IPROYAL_PASS = os.environ.get('IPROYAL_PW')

IPROYAL_USER="plural2356"
IPROYAL_PASS="dorbu7r62t9k"
# Tor proxy settings


app = Flask(__name__)
app.config["output_li"] = []

UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])

# SqlAlchemy Database Configuration With Mysql
app.config["SECRET_KEY"] = "sdfsf65416534sdfsdf4653"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
secure_type = "http"

tor_proxy = r'http://'+f'{IPROYAL_USER}:{IPROYAL_PASS}@geo.iproyal.com:12321'

async def make_tor_request(url):
    try:
        querystring = {
            "show":"listpricerange",
            "by":"offers inventoryTypes accessibility section",
            "apikey":"b462oi7fic6pehcdkzony5bxhe",
            "apisecret":"pquzpfrfz7zd2ylvtz3w5dtyse"
            }
        payload = ""
        headers = {
            'User-Agent':choice(UA),
            'Accept': "*/*",
            'Accept-Language': "en-US,en;q=0.5",
            'Accept-Encoding': "gzip, deflate, br",
            'Origin': "https://www.ticketmaster.com",
            'Connection': "keep-alive",
            'Referer': "https://www.ticketmaster.com/",
            'Sec-Fetch-Dest': "empty",
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Site': "same-site",
        }
        flag = True
        async with ClientSession() as session:
         while flag:             
           async with session.post(url,proxy=tor_proxy, headers=headers, data=payload, params=querystring) as response:
            response_text =  (await response.text())
            if response_text: 
             print(response_text)
             response_text =(response_text)
             print("Response",response.url)
             
             meta_value = response_text.get("title", "nothing")
             if meta_value!="403 Internal Error" and meta_value!="It's not you - it's us":
                app.config["output_li"].append(response_text)
                flag=False 

    except Exception as e:
        raise e
        print(e)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def delete_text_file(file_path):
    try:
      file_path_new = os.path.abspath("result.json")
      os.remove(file_path_new)
    except:
       pass


@app.route("/ticketmaster", methods=["GET", "POST"])
async def ticketmaster():
    print(tor_proxy)
    try:
        input_data = request.files['file']
        path = app.config["UPLOAD_FOLDER"]
        app.config["output_li"] = []

        delete_text_file("result.json")
        delete_text_file("/static/uploads/event_id.csv")
        delete_text_file("event_id.csv")

        if 'file' not in request.files:
            flash('No file part')
            redirect(url_for('home_file', _external=True, _scheme=secure_type))

        if input_data.filename == '':
            flash('No resume selected for uploading')
            redirect(url_for('home_file', _external=True, _scheme=secure_type))

        exten = ""
        if input_data and allowed_file(input_data.filename):
            filename = secure_filename(input_data.filename)
            exten = filename.split(".")[-1]
            input_data.save(filename)
            input_data_path = filename

            session["input_data_path"] = input_data_path
        else:
            flash('This file format is not supported.....')
            redirect(url_for('home', _external=True, _scheme=secure_type))

        if exten:
            if exten=="csv":
                df = pd.read_csv(session["input_data_path"], header=None, skiprows=1, names=["event_id"])
            else:
                df = pd.read_excel(session["input_data_path"], header=None, skiprows=1, names=["event_id"])

        start_time = time.time()
        data = list(df["event_id"])
    
        [(await make_tor_request( f"https://offeradapter.ticketmaster.com/api/ismds/event/{ev}/facets")) for ev in data]                  
        json_data = app.config["output_li"]
        with open("result.json", "w") as json_file_dump:
            json.dump(json_data, json_file_dump)
        print(f"total time {time.time()-start_time}")

        message = f"Process Completed. Please download your output file using Download button\nTime taken for that process {time.time()-start_time}"

        return {"message": message, "response":json_data}

    except Exception as e:
        raise e
        print("Error:",e)
        message = "Server Not Responding"
        return jsonify(message=message)



@app.route("/", methods=["GET", "POST"])
def home():
    try:
        return render_template("index.html")

    except Exception as e:
        print(e)
        return render_template("index.html")

@app.route("/download_logs", methods=['GET'])
def download_logs():
    file = os.path.abspath("result.json")
    return send_file(file, as_attachment=True)


if __name__ == "__main__":
    app.run()
