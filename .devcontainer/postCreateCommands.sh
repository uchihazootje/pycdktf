poetry config virtualenvs.in-project true --local
make install
echo "127.0.0.1     $HOSTNAME" | tee -a /etc/hosts
