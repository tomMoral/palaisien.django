soem command to release on fly.io

Log in the ssh console:
/home/temp/.fly/bin/flyctl ssh console

Transfert files:
/home/temp/.fly/bin/flyctl ssh sftp shell

Deploy the docker image:
/home/temp/.fly/bin/flyctl deploy
