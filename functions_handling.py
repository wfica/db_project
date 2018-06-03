import psycopg2
import json

from consts_and_utils import (SECRET)
from hierarchy import (is_ancestor_of, higher_or_equal)


def handle_root(secret, newpassword, data, emp, cur):
    """Executes function: root <secret> <newpassword> <data> <emp>"""

    if secret != SECRET:
        raise Exception('wrong secret')
    cur.execute(
        """INSERT INTO employee(id, passwd, data) VALUES
    (%s,crypt(%s, gen_salt('bf')), %s);""", (emp, newpassword, data))
    print('{ "status": "OK" }')


def check_passwd(user, passwd, cur):
    """Checks if passwd matches users's password.
    Returns True/False."""

    cur.execute(
        """SELECT id FROM employee WHERE id = %s AND passwd = crypt(%s, passwd);""", (user, passwd))
    return cur.fetchone() is not None


def handle_new(admin, passwd, data, newpasswd, emp1, emp, cur, dfsTimes=None):
    """Executes function: new <admin> <passwd> <data> <newpasswd> <emp1> <emp> """

    if dfsTimes is not None and higher_or_equal(admin, emp1, dfsTimes) == False:
        raise Exception(
            '%s is not entitled to execute new(super=%s, empl=%s)' % (admin, emp1, emp))
    cur.execute(
        """INSERT INTO employee(id, passwd, data, supervisor_id) VALUES
    (%s,crypt(%s, gen_salt('bf')), %s, %s);""", (emp, newpasswd, data, emp1))
    print('{ "status": "OK" }')


def handle_remove(admin, passwd, emp, cur, dfsTimes):
    """Executes function: remove <admin> <passwd> <emp>"""

    if is_ancestor_of(admin, emp, dfsTimes) == False:
        raise Exception('%s is not entitled to remove %s' % (admin, emp))
    cur.execute(
        """DELETE FROM employee WHERE id = %s""", (emp,))
    print('{ "status": "OK" }')


def handle_child(admin, passwd, emp, cur, dfsTimes):
    """Executes function: child <admin> <passwd> <emp>"""

    cur.execute("""SELECT id FROM employee WHERE supervisor_id = %s""", (emp,))
    children = list(map(lambda k: str(k[0]), cur.fetchall()))
    print(json.dumps({"status": "OK", "data": children}))


def handle_parent(admin, passwd, emp, cur, dfsTimes):
    """Executes function: parent <admin> <passwd> <emp>"""

    cur.execute("""SELECT supervisor_id FROM employee WHERE id = %s""", (emp,))
    parent = cur.fetchone()[0]
    if parent is None:
        raise Exception('root has no parent')
    print(json.dumps({"status": "OK", "data": [parent]}))


def handle_ancestors(admin, passwd, emp, cur, dfsTimes):
    """Executes function: ancestors <admin> <passwd> <emp>"""

    ancestors = list(filter(lambda key: is_ancestor_of(
        key, emp, dfsTimes), dfsTimes.keys()))
    print(json.dumps({"status": "OK", "data": ancestors}))


def handle_descendants(admin, passwd, emp, cur, dfsTimes):
    """Executes function: descendants <admin> <passwd> <emp>"""

    descendants = list(filter(lambda key: is_ancestor_of(
        emp, key, dfsTimes), dfsTimes.keys()))
    print(json.dumps({"status": "OK", "data": descendants}))


def handle_ancestor(admin, passwd, emp1, emp2,  cur, dfsTimes):
    """Executes function: ancestor <admin> <passwd> <emp1> <emp2>"""

    check = is_ancestor_of(emp2, emp1, dfsTimes)
    print(json.dumps({"status": "OK", "data": [check]}))


def handle_read(admin, passwd, emp, cur, dfsTimes):
    """Executes function: read <admin> <passwd> <emp>"""

    if higher_or_equal(admin, emp, dfsTimes) == False:
        raise Exception("%s is not entitled to read %s's data" % (admin, emp))
    cur.execute(
        """SELECT data FROM employee WHERE id = %s""", (emp,))
    data = cur.fetchone()[0]
    print(json.dumps({"status": "OK", "data": [data]}))


def handle_update(admin, passwd, emp, newdata, cur, dfsTimes):
    """Executes function: update <admin> <passwd> <emp> <newdata>"""

    if higher_or_equal(admin, emp, dfsTimes) == False:
        raise Exception("%s is not entitled to change %s's data" % (admin, emp))
    cur.execute(
        """UPDATE employee SET data = %s WHERE id = %s""", (newdata, emp))
    print('{ "status": "OK" }')
