import json
import psycopg2
import sys

from consts_and_utils import (SECRET)


def handle_root(args, conn):
    """Executes function: root <secret> <newpassword> <data> <emp>"""

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
    """Checks if passwd matches users's password.
        Returns True/False."""

    cur = conn.cursor()
    cur.execute(
        """SELECT id FROM employee WHERE id = %s AND passwd = crypt(%s, passwd);""", (user, passwd))
    check = True
    if cur.fetchone() == None:
        check = False
    cur.close()
    return check


def handle_new(args, conn, dfsTree=None):
    """Executes function: new <secret> <newpassword> <data> <emp>"""

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


def dfs(supervisor_id, conn, dict, time):
    """ Computes standard pre-order and post-order times of a dfs traverse of 
    the employees graph. It builds dictionary - {employee:(pre-order time, post-order time)}
    The function works in a 'functional' manner accumulating the dictionary.

    Arguments:
    supervisor_id - employee's id whose descendants graph is traversed by the dfs
    conn - connection to the database
    dict - 'so far' constructed dictionary
    time - 'current' time

    Returns: (dict, maxtime) where
    dict - a dictionary which maps employee's id to pair (pre-order time, post-order time)
    maxtime - maximum time in dict + 1"""

    dict[supervisor_id] = (time, None)
    time += 1
    cur = conn.cursor()
    cur.execute(
        """SELECT id FROM employee WHERE supervisor_id = %s""", (supervisor_id,))
    for id in cur:
        dict, time = dfs(id[0], conn, dict, time)
    in_time, _ = dict.pop(supervisor_id)
    dict[supervisor_id] = (in_time, time)
    time += 1
    return dict, time


def preOrder_postOrder_mapping(conn):
    """Computes standard pre-order and post-order times of a dfs traverse of the employees graph. 
    Returns dictionary - {employee:(pre-order time, post-order time)}"""
    
    cur = conn.cursor()
    cur.execute(
        """SELECT id FROM employee WHERE supervisor_id IS NULL;""")
    boss_id = cur.fetchone()[0]
    in_out_times, _ = dfs(boss_id, conn, {}, 1)
    return in_out_times
