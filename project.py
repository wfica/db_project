#!/usr/bin/python2.4
#
# Small script to show PostgreSQL and Pyscopg together
#
import json
import psycopg2
import sys

INIT = 'init'
APP = 'app'
PASSWD = 'qwerty'
SECRET = 'qwerty'


def fail():
    print('{ "status": "ERROR" }')
    return None


def connect(authData):
    conn = psycopg2.connect(
        dbname=authData['database'],
        host='localhost',
        user=authData['login'],
        password=authData['password'])
    return conn


def initialize_db(authData):
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
    cur.close()
    return conn


def handle_first_line():
    jsonObj = json.loads(sys.stdin.readline())
    try:
        if jsonObj['open']['login'] == INIT:
            conn = initialize_db(jsonObj['open'])
        else:
            conn = connect(jsonObj['open'])
        conn.commit()
        print('{ "status": "OK" }')
        return conn
    except:
        fail()


def handle_root(args, conn):
    if args['secret'] != SECRET:
        raise Exception('wrong secret')
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO employee(id, passwd, data) VALUES
        (%s,crypt(%s, gen_salt('bf')), %s);""", (args['emp'], args['newpassword'], args['data']))
    conn.commit()


def handle_line(line, conn):
    jsonObj = json.loads(line)
    function = list(jsonObj.keys())[0]
    args = jsonObj[function]
    if function == 'root':
        handle_root(args, conn)


def main():
    conn = handle_first_line()
    for line in sys.stdin.readlines():
        try:
            handle_line(line, conn)
        except Exception as e:
            print(e)
            fail()


if __name__ == '__main__':
    main()
