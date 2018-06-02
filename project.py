import json
import psycopg2
import sys
import functions_handling as fh
from consts_and_utils import (fail, DEBUG)
from db_initialization import (handle_first_line)


def handle_line(line, conn):
    jsonObj = json.loads(line)
    function = list(jsonObj.keys())[0]
    args = jsonObj[function]
    if function == 'root':
        fh.handle_root(args, conn)
    elif function == 'new':
        fh.handle_new(args, conn)


def main():
    conn = handle_first_line()
    if len(sys.argv) == 1:
        tree = fh.preOrder_postOrder_mapping(conn)
        print(tree)
    for line in sys.stdin.readlines():
        try:
            handle_line(line, conn)
        except Exception as e:
            if DEBUG: 
                print(e)
            fail()
        finally:
            conn.commit()

if __name__ == '__main__':
    main()
