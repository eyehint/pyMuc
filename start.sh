#!/bin/sh
export PYTHONPATH=$(pwd)
twistd3 -n --reactor=epoll -y server.py