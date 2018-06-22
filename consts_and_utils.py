from hierarchy import dfs

INIT = 'init'
APP = 'app'
PASSWD = 'qwerty'
SECRET = 'qwerty'
DEBUG = False

def fail():
    print('{ "status": "ERROR" }')
    return None

def preOrder_postOrder_mapping(conn):
    """Computes standard pre-order and post-order times of a dfs traverse of the employees graph. 
    Returns dictionary - {employee's id : (pre-order time, post-order time)}"""

    cur = conn.cursor()
    cur.execute(
        """SELECT id FROM employee WHERE supervisor_id IS NULL;""")
    boss_id = cur.fetchone()[0]
    in_out_times, _ = dfs(boss_id, conn, {}, 1)
    return in_out_times
