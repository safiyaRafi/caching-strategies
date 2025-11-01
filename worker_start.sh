#!/bin/sh
# Wait for redis
sleep 3
rq worker --url redis://redis:6379/0 default