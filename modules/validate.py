#import modules.dbconnect as dbconnect
from . import dbconnect
#import dbconnect

def validateUser(user,pwd):
    db,cursor,ret_code = dbconnect.conn()
    if ret_code != 200:
        return None, 400

    sql = 'SELECT UsersPassword from users where UsersUsername = "%s"' %(user)
    print(sql) 
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)
    if result == None or not len(result):
        print("user doesnot exist")
        return "user doesnot exist", 400
    if result[0] != pwd:
        print("Password Incorerct")
        return "password Incorrect", 400
    print("Login Success")
    return "LoginSuccess", 200

#validateUser("superuser","WU3kd-DJM_uf")
