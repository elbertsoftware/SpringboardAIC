from cassandra.cluster import Cluster

if __name__ == "__main__":
    #cluster = Cluster(['localhost'], port=9042)  # cas1 node
    cluster = Cluster(['localhost'], port=9043)  # cas2 node
    session = cluster.connect('CityInfo', wait_for_all_pools=True)
    session.execute('USE "CityInfo"')
    rows = session.execute('SELECT * FROM users')
    for row in rows:
        print(row.age, row.name, row.username)