import psycopg2


def is_ancestor_of(supervisor_id, empl_id, dict):
    """Checks if supervisor_id is supervisor of empl_id"""
    
    sin, sout = dict[supervisor_id]
    ein, eout = dict[empl_id]
    return (sin < ein and sout > eout)

def higher_or_equal(supervisor_id, empl_id, dict):
    """Checks if supervisor >= empl"""

    return supervisor_id == empl_id or is_ancestor_of(supervisor_id, empl_id, dict)

def dfs(supervisor_id, conn, dict, time):
    """ Computes standard pre-order and post-order times of a dfs traverse of 
    the employees graph. It builds dictionary - {employee:(pre-order time, post-order time)}
    The function works in a 'functional' manner by accumulating the dictionary.

    Arguments:\n
    supervisor_id - employee's id whose descendants graph is traversed by the dfs\n
    conn - connection to the database\n
    dict - 'so far' constructed dictionary\n
    time - 'current' time\n

    Returns: (dict, maxtime) where\n
    dict - a dictionary which maps employee's id to pair (pre-order time, post-order time)\n
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

