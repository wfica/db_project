import json
import psycopg2
import sys
import functions_handling as fh
from consts_and_utils import (fail, DEBUG, preOrder_postOrder_mapping)
from db_initialization import (handle_first_line)


def handle_line(line, cur, dfsTimes):
    """Executes a function from the input line"""

    if line == "" or line == "\n":
        return
    jsonObj = json.loads(line)
    function = list(jsonObj.keys())[0]
    args = jsonObj[function]
    if function == 'root':
        fh.handle_root(args['secret'], args['newpassword'], args['data'], args['emp'], cur)
        return

    admin = args['admin']
    passwd = args['passwd']
    if 'emp' in args:
        fargs = [admin, passwd, args['emp'], cur, dfsTimes]

    if fh.check_passwd(admin, passwd, cur) == False:
        raise Exception('wrong password')
    
    if function == 'new':
        fh.handle_new(admin, passwd, args['data'], args['newpasswd'], args['emp1'], args['emp'], cur)
    elif function == 'ancestor':
        fh.handle_ancestor(admin, passwd, args['emp1'], args['emp2'], cur, dfsTimes)
    elif function == 'remove':
        fh.handle_remove(*fargs)
    elif function == 'child':
        fh.handle_child(*fargs)
    elif function == 'parent':
        fh.handle_parent(*fargs)
    elif function == 'ancestors':
        fh.handle_ancestors(*fargs)
    elif function == 'descendants':
        fh.handle_descendants(*fargs)
    elif function == 'read':
        fh.handle_read(*fargs)
    elif function == 'update':
        fh.handle_update(admin, passwd, args['emp'], args['newdata'], cur, dfsTimes )

def main():
    conn, user = handle_first_line()
    cur = conn.cursor()
    if user != 'init':
        dfsTimes = preOrder_postOrder_mapping(conn)
        print(dfsTimes)
    for line in sys.stdin.readlines():
        try:
            handle_line(line, cur, dfsTimes)
        except Exception as e:
            if DEBUG: 
                print(e)
            fail()
        finally:
            conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
