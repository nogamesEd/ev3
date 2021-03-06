#!/usr/bin/env python3

# Nasty WSGI startup stuff, stolen from https://www.khalidalnajjar.com/developing-blazing-fast-website-python-using-falcon-bjoern/
# Probably not worth touching. Take a look at app.py instead.

import bjoern
from ipaddress import ip_address
from app import HardwareAPI
from ev3dev.ev3 import Sound
 
wsgi_app = HardwareAPI
 
if __name__ == '__main__':
    import argparse # for parsing passed parameters through terminal
 
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", help="Hostname", default='0.0.0.0:8000', nargs='?') # either define an IP
    parser.add_argument("-socket", help="Linux Socket Name", default=None, nargs='?') # or pass path of Linux's socket
    args = parser.parse_args()
 
    if args.socket: # a socket is passed
        bjoern.run(wsgi_app, 'unix:' + args.socket)
    else:
        if ':' in args.ip:
            ip, separator, port = args.ip.rpartition(':')
            ip = ip_address(ip.strip("[]"))
            port = int(port)
        else:
            ip = ip_address(args.ip.strip("[]"))
            port = 8000
        ip = str(ip)
        print("Starting server on {}:{}".format(ip, port))
        Sound.beep()
        bjoern.run(wsgi_app, ip, port)
