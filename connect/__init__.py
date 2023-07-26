import argparse

from connect.mysql_client import MysqlClient

parser = argparse.ArgumentParser(description="cicd")
parser.add_argument(
    "--mysql_host",
    type=str,
)
parser.add_argument(
    "--mysql_port",
    type=int,
)
parser.add_argument(
    "--mysql_user",
    type=str,
)
parser.add_argument(
    "--mysql_password",
    type=str,
)
args, _ = parser.parse_known_args()
mysql_host = args.mysql_host or "82.157.239.83"
mysql_port = args.mysql_port or 3000
mysql_user = args.mysql_user or "root"
mysql_password = args.mysql_password or "JJfkP4bSZ"
mysql_client = MysqlClient(mysql_host, mysql_port, mysql_user, mysql_password)
