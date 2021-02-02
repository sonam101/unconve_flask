##!/usr/bin/python

import MySQLdb
def conn():
    # Open database connection
    try:
        db = MySQLdb.connect("localhost","dummy_user","dummy_pwd","dummy_db" )
        cursor = db.cursor()
        #print('success')
        return db,cursor,200
    except:
        print('fail to connect to db')
        return "failure",None, 400

#conn()
