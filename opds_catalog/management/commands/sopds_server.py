import os
import signal
import sys
import socket
import errno
import django

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command, ManagementUtility
from django.core.servers.basehttp import get_internal_wsgi_application, run
from django.utils.encoding import force_text
from django.core.handlers.wsgi import WSGIHandler

from opds_catalog.settings import SERVER_LOG

class Command(BaseCommand):
    help = 'HTTP/OPDS built-in server'

    def add_arguments(self, parser):
        parser.add_argument('command', help='Use [ start | stop | restart ]')
        parser.add_argument('--host',action='store', dest='host', default="0.0.0.0", help='Set server binding address')
        parser.add_argument('--port',action='store', dest='port', default=8001, help='Set server port')
        parser.add_argument('--daemon',action='store_true', dest='daemonize', default=False, help='Daemonize server')


    def handle(self, *args, **options):
        self.pidfile = os.path.join(settings.BASE_DIR, "sopds-server.pid")
        action = options['command']
        self.addr = options['host']
        self.port = int(options['port'])
        
        if (options["daemonize"] and (action == "start")):
            if sys.platform == "win32":
                print("On Windows platform Daemonize not working.")
            else:         
                daemonize()
                
        if action == "start":
            self.start()
        elif action == "stop":
            pid = open(self.pidfile, "r").read()
            self.stop(pid)
        elif action == "restart":
            pid = open(self.pidfile, "r").read()
            self.restart(pid)
                      
    def start(self):
        writepid(self.pidfile)
        call_command('runserver',addrport='%s:%s'%(self.addr,self.port), use_reloader=False, app_label='opds_catalog')

    def stop(self, pid):
        try:
            os.kill(int(pid), signal.SIGTERM)
        except OSError as e:
            print(str(e))

    def restart(self, pid):
        self.stop(pid)
        self.start()

def writepid(pid_file):
    """
    Write the process ID to disk.
    """
    fp = open(pid_file, "w")
    fp.write(str(os.getpid()))
    fp.close()

def daemonize():
    """
    Detach from the terminal and continue as a daemon.
    """
    # swiped from twisted/scripts/twistd.py
    # See http://www.erlenstar.demon.co.uk/unix/faq_toc.html#TOC16
    if os.fork():   # launch child and...
        os._exit(0) # kill off parent
    os.setsid()
    if os.fork():   # launch child and...
        os._exit(0) # kill off parent again.
    os.umask(0)

    std_in = open("/dev/null", 'r')
    std_out = open(SERVER_LOG, 'a+')
    os.dup2(std_in.fileno(), sys.stdin.fileno())
    os.dup2(std_out.fileno(), sys.stdout.fileno())
    os.dup2(std_out.fileno(), sys.stderr.fileno())    
    
#    null = os.open("/dev/null", os.O_RDWR)
#    for i in range(3):
#        try:
#            os.dup2(null, i)
#        except OSError as e:
#            if e.errno != errno.EBADF:
#                raise
    os.close(std_in.fileno())
    os.close(std_out.fileno())


