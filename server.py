#!/usr/bin/env python3

import time
import os
import requests
import logging
import re
import socket
import sqlite3
from flask import Flask, request, render_template
from werkzeug.exceptions import abort

start = time.time()
hostname = os.environ.get('HOSTNAME')
version = os.environ.get('VERSION')

logger = logging.getLogger(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)

@app.route("/")
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route("/cowsay")
def build_cow():
    return """
    [Quark Server]
         \   ^__^ 
          \  (oo)\_______
             (__)\       )\/\\\\
                 ||----w |
                 ||     ||
    """

@app.route("/healthz")
def get_healthz():
    if start < time.time():
        return 'ok'
    return 'no'

@app.route("/hello")
def get_hello():
    message = "Hello world, today is {}".format(time.ctime())
    logger.info(message)
    return message 

@app.route("/date")
def get_date():
    return time.ctime()

@app.route("/sleep")
def get_sleep():
    return start_sleep(5)

@app.route("/sleep/<num>")
def get_sleep_num(num):
    return start_sleep(num)

def start_sleep(num):
    logger.info(time.ctime())
    time.sleep(int(num))
    logger.info(time.ctime())
    return "You has been waiting for {} seconds".format(time.ctime())

@app.route("/error")
def get_error():
    return 'Error', 503

@app.route("/version")
def get_version():
    return version 

@app.route("/tcp", methods=['GET'])
def get_tcp():
    host = set_host(request.args.get('host'))
    port = set_port(request.args.get('port'))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex((host, int(port)))
        s.close()
        if result:
            message = "Error connection tcp to {}:{}".format(host, port)
        else:
            message = "Successfull connetion tcp to {}:{}".format(host, port)
    return render_template('testconn.html', date=time.ctime(), message=message)

def set_host(host):
    if host == None or host == "":
        host = "127.0.0.1"
    return str(host)

def set_port(port):
    if port == None or port== "":
        port = int(8080)
    return int(port)

def set_service_type(service_type):
    if service_type == None or service_type == "":
        service_type = "end"
    return service_type
     
@app.route("/forward", methods=['GET'])
def get_forward():
    service_type = set_service_type(request.args.get('type'))
    host = set_host(request.args.get('host'))
    port = set_port(request.args.get('port'))
    if service_type == 'pass':
        message = forward(request.headers, host, int(port))
    elif service_type == 'end':
        message = "{} is the end of chain of services".format(os.environ.get('HOSTNAME'))
    else:
        message = "Type parameter is not defined and is required"
    logger.debug(message)
    return message

def forward(headers, host, port):
    url = "http://{}:{}/".format(host, port)
    present = requests.get(url, headers=prepare_outbound_headers(headers))
    message = "Forwarding http request from {} to {}:{}, time_elapsed {}, status_code {}".format(
        os.environ.get('HOSTNAME'), host, port, present.elapsed, present.status_code)
    logger.info(message)
    return message, present.status_code
 
def prepare_outbound_headers(inbound_headers):
    # Zipkins headers to tracing
    # https://github.com/openzipkin/b3-propagation
    outbound_headers = {}
    outbound_headers['Authorization'] = inbound_headers.get('Authorization')
    outbound_headers['x-request-id'] = inbound_headers.get('x-request-id')
    outbound_headers['x-b3-traceid'] = inbound_headers.get('x-b3-traceid')      
    outbound_headers['x-b3-spanid'] = inbound_headers.get('x-b3-spanid')
    outbound_headers['x-b3-parentspanid'] = inbound_headers.get('x-b3-parentspanid')
    outbound_headers['x-b3-sampled'] = inbound_headers.get('x-b3-sampled')
    outbound_headers['x-b3-flags'] = inbound_headers.get('x-b3-flags')
    return outbound_headers

@app.route("/url")
def get_url():
    host = set_host(request.args.get('host'))
    port = set_port(request.args.get('port'))
    if port == None: 
        port = 80
    url = "http://{}:{}".format(str(host),str(port))
    try:
        response = requests.get(url)
        status_code = response.status_code
        if status_code == 200:
            message = "Success response HTTP to {}:{} with status code {}".format(host, port, status_code)
        else:
            message = "Error response HTTP to {}:{} with status code {}".format(host, port, status_code)
        return render_template('url.html', date=time.ctime(), message=message)
    except:
        return version, status_code 

@app.route("/logger/<num>")
def get_logger(num):
    i = 0
    print("Date {} and waiting for {} seconds".format(time.ctime(), num))
    while(i <= int(num)):
        print("Date {} and pass the second numer {} seconds".format(time.ctime(), i))
        time.sleep(1)
        i+=1
    message = "Date {} and finalize and counter {} reach {} seconds".format(time.ctime(), num, i)
    print(message)
    return message 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
