import time
import os
import logging
import socket
import sqlite3
import requests
from flask import Flask, request, render_template, url_for, flash, redirect
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from werkzeug.exceptions import abort
from prometheus_client import make_wsgi_app, Counter, Histogram

start = time.time()
hostname = os.environ.get('HOSTNAME')
version = os.environ.get('VERSION')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_super_secret_key'

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

# Quark blog post
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

@app.route('/create', methods=('GET', 'POST'))
def create():
    ''' POST: Create a reminder post with the data of the form '''
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', 
                        (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!', 'warning')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']), 'info')

    return redirect(url_for('index'))


@app.route("/tcp", methods=('GET', 'POST',))
def tcp_check():
    """ Check TCP Socker is Open and return a message   """
    message = "Please complete ip addres and port"

    if request.method == 'POST':
        host = request.form['host']
        port = request.form['port']

        if not host or not port:
            flash('Host and port is required!', 'warning')
        else:
            result = socket_check(host, port)
            print(result)
            if result:
                message = "Error tcp connection: {}:{}".format(host, port)
                flash(message, 'error')
            else:
                message = "Successfull tcp connetion: {}:{}".format(host, port)
                flash(message, 'info')

    return render_template('tcp.html')


def socket_check(host, port):
    """ Check TCP Socket """
    socket.setdefaulttimeout(1)
    socket_device = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return socket_device.connect_ex((host, int(port)))


@app.route("/cowsay")
def build_cow():
    """ Return greating to see in terminal """
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
    """ Get to health check """ 
    if start < time.time():
        return 'ok'

    return 'no'


@app.route("/date")
def get_date():
    """ Get that return the date """

    return time.ctime()


@app.route("/sleep")
def get_sleep():
    """ Trigger sleep time in secods"""

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


@app.route("/forward", methods=['GET'])
def get_forward():
    service_type = request.args.get('type')
    host = request.args.get('host')
    port = request.args.get('port')
    if service_type == 'pass':
        message = forward(request.headers, host, int(port))
    elif service_type == 'end':
        message = "{} is the end of chain of services".format(
            os.environ.get('HOSTNAME'))
    else:
        message = "Type parameter is not defined and is required"
    logger.debug(message)

    return message

def forward(headers, host, port):
    url = "http://{}:{}/".format(host, port)
    present = requests.get(url, headers=prepare_outbound_headers(headers))
    message = "Forwarding http request from {} to {}:{}, time_elapsed {}, status_code {}".format(
        os.environ.get('HOSTNAME'),
        host, port, present.elapsed, present.status_code)
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
def check_url():
    ''' TODO refactor Test HTTP connection '''
    host = request.args.get('host')
    port = request.args.get('port')
    if port == None: 
        port = 80
    url = "http://{}:{}".format(str(host),str(port))
    response = get_url_monitor(url, request)
    status_code = response.status_code
    if status_code == 200:
        message = "Success response HTTP to {}:{} with status code {}".format(host, port, status_code)
    else:
        message = "Error response HTTP to {}:{} with status code {}".format(host, port, status_code)
    return render_template('url-response.html', date=time.ctime(), message=message)

def get_url_monitor(url, request):
    try:
        before_request(request)
        response = requests.get(url)
        after_request(response)
        return response
    except:
        return response, version

# Prometheus metrics 
HISTOGRAM = Histogram('quark_request_latency_seconds', 'Quark request latency', ['method', 'endpoint'])
COUNTER = Counter('quark_request_count', 'Quark request count', ['method', 'endpoint', 'http_status'])

def before_request(request):
	request.start_time = time.time()

def after_request(response):
	request_latency = time.time() - request.start_time
	HISTOGRAM.labels(request.method, request.path).observe(request_latency)
	COUNTER.labels(request.method, request.path, response.status_code).inc()

	return response


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


if __name__ == '__main__':
    run_simple('0.0.0.0', 8080, app.wsgi_app, use_reloader=True, use_debugger=True, use_evalex=True)
