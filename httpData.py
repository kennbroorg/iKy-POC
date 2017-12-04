#!/usr/bin/env python
# -*- coding: utf-8

import argparse
import socket
import json
from flask import Flask, render_template, request
from src import osint


def validate_address_port(address, port):
    """
    Validate IP address and port
    """

    try:
        socket.inet_aton(address)
    except socket.error:
        raise argparse.ArgumentTypeError(
            "%s is not a valid IP address" % address)

    if (port < 0) or (port > 65535):
        raise argparse.ArgumentTypeError(
            "%s is not a valid port number" % port)

    return address, port


app = Flask(__name__)


@app.route('/')
def initial_page():
    """
    Show the initial page
    """

    return render_template('index.html')


@app.route('/dataCollect', methods=['POST'])
def data_collect():
    """
    Show the results of the OSINT proccess
    """

    datas = osint.osint_process(request.form['email'])
    jsondata = json.loads(datas)

    return render_template('dataGraph.html', jsondata=json.dumps(jsondata))


if __name__ == '__main__':

    parser_args = argparse.ArgumentParser()
    parser_args.add_argument('-i', '--ip', dest='ip', default='127.0.0.1',
                             help='IP address the server will listen on')
    parser_args.add_argument('-p', '--port',
                             help="Port the server will listen on", type=int,
                             default='5500')

    args = parser_args.parse_args()
    address, port = validate_address_port(args.ip, args.port)

    app.run(host=address, port=port)
