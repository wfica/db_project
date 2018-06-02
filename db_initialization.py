import json
import psycopg2
import sys
from consts_and_utils import (fail, INIT, APP, PASSWD)

def connect(authData):
    """Returns connection to the database."""

    conn = psycopg2.connect(
        dbname=authData['database'],
        host='localhost',
        user=authData['login'],
        password=authData['password'])
    return conn


def initialize_db(authData):
    """Creates TABLE employee and ROLE app.
    Grants SELECT, DELETE, UPDATE, INSERT ON employee TO app."""

    conn = connect(authData)
    cur = conn.cursor()
    cur.execute(
        """DROP TABLE IF EXISTS employee;""")
    cur.execute(
        """CREATE TABLE employee(
            id int PRIMARY KEY,
            passwd text not null, 
            data text,
            supervisor_id int REFERENCES employee(id) ON DELETE CASCADE );""")

    cur.execute(
    """SELECT    *
       FROM   pg_catalog.pg_roles
       WHERE  rolname = %s;""", (APP,))

    if cur.fetchone() == None:
        cur.execute(
        """CREATE ROLE %s LOGIN PASSWORD %s;""", (APP, PASSWD))

    cur.execute(
    """GRANT SELECT, DELETE, UPDATE, INSERT ON employee TO app ;""", (APP,))
    # Psycopg adds quotes around app when %s is used insted of literal ??!!!
    # print(cur.mogrify("""GRANT SELECT ON employee TO %s;""", (APP,)))

    cur.close()
    return conn


def handle_first_line():
    """Handles first line of an input - returns connection to the db.
    If it's init then db will be initialized."""

    jsonObj = json.loads(sys.stdin.readline())
    try:
        if jsonObj['open']['login'] == INIT:
            conn = initialize_db(jsonObj['open'])
        else:
            conn = connect(jsonObj['open'])
        conn.commit()
        print('{ "status": "OK" }')
        return conn, jsonObj['open']['login']
    except:
        fail()
