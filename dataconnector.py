import psycopg2
import binascii
import sys
import socket

exporters = []

try:
    conn = psycopg2.connect(host="10.30.70.70", database="plixer",
                            user="scrutremote", password="admin")
except:
    print "I am unable to connect to the database"


def get_exporters():
	cur = conn.cursor()
	cur.execute("""select inet_b2a(exporter_id) from plixer.distributed_exporters""")
	rows = cur.fetchall()
	exporters = [item for items in rows for item in items]
	return(exporters)

def convert_exporter(ipaddress):
	converted_ip = 'in_' + str.upper(str(binascii.hexlify(socket.inet_aton(ipaddress)).decode())) + '_' + 'ALL'

	return(converted_ip)


print(convert_exporter('10.1.1.1'))









