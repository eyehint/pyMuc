#!/bin/sh
~/bin/psython2.7 ~/bin/twistd -n  --reactor=epoll -y server.py
