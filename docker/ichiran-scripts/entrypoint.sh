#!/bin/bash

echo "Checking postgres server status..."
while : ; do
    pg_isready -h pg > /dev/null && break;
    sleep 1;
done

echo "Postgres is ready, starting main container init."
init-all;

python /root/quicklisp/local-projects/ichiran/server.py --port 5000 --max-size 10 &

echo "All set, awaiting commands."
sleep infinity;