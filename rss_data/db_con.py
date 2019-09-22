import sqlite3
from sqlite3 import Error
from get_data import get_data_json
import pandas as pd 

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn
 
 
 
def create_entry(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
 
    sql = ''' INSERT INTO news(guid,link,pubDate,author,description,title,fid)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, task)
        return cur.lastrowid
    except Exception as e:
        #print(e)
        return None
 
def main():
    database = "./pythonsqlite.db"
    insert_count = 0
    error_count = 0
    # create a database connection
    conn = create_connection(database)
    keys = ["guid","link","pubDate","author","description","title"]
    with conn:
        feed_list = pd.read_csv("feed_list.csv")
        for index,row in feed_list.iterrows():
            fid = row["index"]
            url = row["link"]
            try:
                dict_data = get_data_json(url)
            except Exception as e:
                print(e)
                continue
            for item in dict_data:
                # create a new entry
                project = []
                for k in keys:
                    if k in item:
                        project.append(item[k])
                    else:
                        project.append("")
                project.append(fid)
                project_id = create_entry(conn, project)
                if project_id:
                    insert_count += 1
                else:
                    error_count += 1
                #print(project_id)
            print(fid)
            print("insert_count",insert_count)
            print("error_count",error_count)
if __name__ == '__main__':
    main()
