import json
import psycopg2
import sys

from consts_and_utils import (SECRET)


def handle_root(args, conn):
    if args['secret'] != SECRET:
        raise Exception('wrong secret')
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO employee(id, passwd, data) VALUES
    (%s,crypt(%s, gen_salt('bf')), %s);""", (args['emp'], args['newpassword'], args['data']))
    conn.commit()
    cur.close()
    print('{ "status": "OK" }')


def check_passwd(user, passwd, conn):
    cur = conn.cursor()
    cur.execute(
        """SELECT id FROM employee WHERE id = %s AND passwd = crypt(%s, passwd);""", (user, passwd))
    check = True
    if cur.fetchone() == None:
        check = False
    cur.close()
    return check


def handle_new(args, conn, dfsTree=None):
    if check_passwd(args['admin'], args['passwd'], conn) == False:
        raise Exception('wrong password')
    if dfsTree is not None:
        raise Exception('has to check hierarchy')
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO employee(id, passwd, data, supervisor_id) VALUES
    (%s,crypt(%s, gen_salt('bf')), %s, %s);""", (args['emp'], args['newpasswd'], args['data'], args['emp1']))
    conn.commit()
    cur.close()
    print('{ "status": "OK" }')
