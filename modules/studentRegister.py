from . import dbconnect

def studentRegister(sname,whatsapp,fname,fno,email,clas):
        #Connect with db
        db, cursor, ret_code = dbconnect.conn()
        if ret_code != 200:
            return None, 400

        sql = 'INSERT INTO students(STUDENT_NAME, WHATSAPP_NO, FATHER_NAME, FATHER_CONTACT_NO, EMAIL_ID, CLASS) VALUES (%s, %s, %s, %s, %s, %s)'
        val = (sname, whatsapp, fname, fno, email, clas)

        cursor.execute(sql, val)
        db.commit()
        db.close()
        return "Succesfully Registered", 200 


def teacherRegister(tname, cno, email, clas, subject):
    #Connect with db
    db, cursor, ret_code = dbconnect.conn()
    if ret_code != 200:
        return None, 400

    sql = 'SELECT SUBJECT_ID FROM subject WHERE SUBJECT_NAME = "%s" '%(subject)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None or not len(result):
        print("Subject is not present")
        return "Subject is not present", 400
    else:
        sql = 'INSERT INTO teachers(TEACHERS_NAME, CONTACT_NO, EMAIL_ID, CLASS, SUBJECT) VALUES(%s, %s, %s, %s, %s)'
    val = (tname, cno, email, clas, result)

    cursor.execute(sql, val)
    db.commit()
    db.close()
    return "Succesfully Registered", 200
