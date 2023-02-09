#!/bin/bash
#chkconfig: 12345 90 10
#description: start topology service
cd /www/ft101/back;nohup gunicorn -c gunicorn.conf.py main:app -k uvicorn.workers.UvicornWorker