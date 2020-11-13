#!/bin/bash
(echo >/dev/tcp/127.0.0.1/8080)&>/dev/null && echo "Openning" >/dev/null  || (source /home/hc/anaconda3/bin/activate vtcc && python ~/Desktop/workplace/python/flask_test.py )
