#!/bin/bash

mkdir -p /usr/local/oracle_keeper
wget  -N --no-check-certificate https://raw.githubusercontent.com/akiiya/Shell/master/oracle_keeper/oracle_keeper.py -O /usr/local/oracle_keeper/oracle_keeper.py
wget  -N --no-check-certificate https://raw.githubusercontent.com/akiiya/Shell/master/oracle_keeper/oracle_keeper.service -O /usr/lib/systemd/system/oracle_keeper.service
chmod +x /etc/systemd/system/oracle_keeper.service
systemctl daemon-reload
systemctl enable oracle_keeper

#nohup python3 oracle_keeper.py > /dev/null 2>&1 &