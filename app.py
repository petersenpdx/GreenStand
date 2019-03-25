from lib.image import TreeImage
import json
import psycopg2
from sshtunnel import SSHTunnelForwarder
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine





# Create an SSH tunnel
tunnel = SSHTunnelForwarder()




#Start the tunnel
tunnel.start()
print(tunnel.local_bind_port)
# Create a database connection
conn = psycopg2.connect()

# Get a data cursor
cur = conn.cursor()

# Print PostgreSQL Connection properties
print(conn.get_dsn_parameters(),"\n")
#
# # Execute SQL
# cur.execute("SELECT * FROM tress, ORDER BY id DESC, LIMIT 5;")
#
# # Print SQL command
#
# record = cur.fetchone()
# print("You are connected to - ", record,"\n")
# conn.close()
# tunnel.stop()


def load_urls(fname):
    """
    This returns a lists only the url column from the .csv file treetracker
    :param fname: .csv file name - specifically all treetracker data from tree table
    :return: url list
    """
    urls = []
    with open("temp.csv", "r") as temp_file:
        content = temp_file.readlines()[1:]

        for item in content:
            urls.append(item.split(',')[1].strip())
    return urls

urls = load_urls("temp.csv")


result = {}

with open('results_f.csv', 'w') as file:

    for url in urls:
        tree = TreeImage(url)
        result = tree.export()
        file.write(json.dumps(result))

        print(result)








