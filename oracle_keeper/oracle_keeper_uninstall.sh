systemctl stop oracle_keeper
systemctl disable oracle_keeper
rm -rf /usr/local/oracle_keeper
rm /usr/lib/systemd/system/oracle_keeper.service
systemctl daemon-reload
