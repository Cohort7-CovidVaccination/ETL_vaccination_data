import requests
import csv
import os
import psycopg2
import queries

def download_csv(url):

    #TODO error manage
    with requests.Session() as s:
        data_req = s.get(url).content.decode('utf-8')
        data = list(csv.reader(data_req.splitlines(), delimiter=','))

    return data

def connect_db():
    con = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        port=os.environ['DB_PORT'])

    return con

if __name__ == '__main__':

    url_country_data = os.environ['URL_COUNTRY_DATA']
    data_countries = download_csv(url_country_data)

    for item in data_countries:
        print(item)
        print(len(item))

    con = connect_db()

    cur = con.cursor()
    cur.execute(queries.create_countries)
    cur.execute(queries.create_registers)
    con.commit()

    cur.close()
    con.close()