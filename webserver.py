import re
import os
import socket
import sys
import thread
import eventlet
import logging
import time
import SocketServer
import subprocess
from functools import wraps
from wsgiref import handlers
from werkzeug import secure_filename
from pydispatch import dispatcher
from multiprocessing import Process
from flask import Flask, render_template, url_for, request, g, redirect, session, flash, Response, send_from_directory
from flask_socketio import SocketIO, emit

# Patch system modules to be greenthread-friendly
eventlet.monkey_patch()

# Another monkey patch to avoid annoying (and useless?) socket pipe warnings when users disconnect
SocketServer.BaseServer.handle_error = lambda *args, **kwargs: None
handlers.BaseHandler.log_exception = lambda *args, **kwargs: None

# Turn off more annoying log messages that aren't helpful.
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__, static_folder='webpage')
app.secret_key = 'B9Zr55a/1rt_R~XZZ?i24]LWX/,?RT'
app.config['UPLOAD_FOLDER'] = app.static_folder
#app.debug=True
socketio = SocketIO(app, async_mode='threading', ping_timeout=30, logger=False, engineio_logger=False)

class WebServer:
    def __init__(self):
        app.adminMode = False

    def start(self,bAdminMode=None,domainName="mvilamp"):
        print "Starting web server"
        app.adminMode = bAdminMode
        app.self = self
        thread.start_new_thread(lambda: socketio.run(app,host='0.0.0.0',port=80), ())
        self.socket = socketio
        app.localDomainName = re.sub(r'\W+', '', domainName)

    def shutdown(self):
        global socketio
        socketio.stop()
        socketio.shutdown(socketio.SHUT_RDWR)
        self.socketio = None
        self.server.terminate()
        self.server.join()

    @app.route("/")
    def index():
        return app.send_static_file('index.html'), 200

    @app.route("/redirect")
    def redirectURL():
    	url = "http://www."+ app.localDomainName + ".com"
        return redirect(url, code=302)

    @app.route("/generate_204")
    def captivePortal():
        print "CAPTIVE PORTAL"
        return ('', 204)

    @app.errorhandler(404)
    def page_not_found(error):
        print request.path
        print "Error 404"
        if app.adminMode:
            return app.send_static_file('admin.html'), 200
        else:
            return app.send_static_file('index.html'), 200

    @app.errorhandler(400)
    def page_error(error):
        print "Error 400?!"
        return "ok", 200

    @app.route('/uploader', methods = ['GET', 'POST'])
    def upload_file():
        print request.method
        if request.method == 'POST':
            print "OK"
            f = request.files['file']
            print f
            print f.filename
            print os.path.join(app.config['UPLOAD_FOLDER'])
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            return 'files uploaded successfully'

    @app.route('/<path:path>')
    def static_proxy(path):
        # send_static_file will guess the correct MIME typen
        return app.send_static_file(path)

    @socketio.on('onConnect')
    def connectEvent(msg):
        dispatcher.send(signal='connectEvent')

    # Broadcast an event over the socket
    def broadcast(self,id,data):
        with app.app_context():
            try:
                socketio.emit(id,data,broadcast=True)
            except:
                pass