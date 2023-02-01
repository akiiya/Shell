systemctl stop oracle_keeper
systemctl disable oracle_keeper
rm /usr/local/oracle_keeper/oracle_keeper.py
rm /usr/lib/systemd/system/oracle_keeper.service
systemctl daemon-reload
