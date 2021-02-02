try:
    from . import dbconnect
except:
    import dbconnect

def get_data(tablename,attributes):
   db, cursor, ret_code = dbconnect.conn()
   if ret_code != 200:
       return db, ret_code
   sql = '''select %s from %s where valid = 1 order by 1''' %(attributes, tablename)
   cursor.execute(sql)
   data  = list(cursor.fetchall())
   data = [list(i) for i in data]
   #print(data)
   return data,200

#get_data('teachers','TEACHERS_ID,TEACHERS_NAME')


def insert_data(subject_id, teacher_id, students_id, date, duration, description_teacher, description_student):
    db, cursor, ret_code =dbconnect.conn()
    if ret_code!= 200:
        return db, ret_code
    sql = 'INSERT INTO routine_teacher(TEACHER_ID, SUBJECT_ID, TIME, DURATION, DESCRIPTION) values(%s, %s, %s, %s, %s)'
    val = (teacher_id, subject_id, date, duration, description_teacher)
    try:
        cursor.execute(sql, val)
        #db.commit()

        sql = 'SELECT MAX(ROUTINE_TEACHER_ID) FROM routine_teacher'
        cursor.execute(sql)
        result = cursor.fetchone()
        if result == None or not len(result):
            return "Failure", 400 #ask Mr. V.Kumar
        else:
            for student in students_id:
                sql = 'INSERT INTO routine_student(ROUTINE_TEACHER_ID, STUDENT_ID, DESCRIPTION) values(%s, %s, %s)'
                val = (result, student, description_student)
                cursor.execute(sql, val)
                #db.commit()
        db.commit()
        db.close()
    except MySQLdb.Error as e:
        print(e)
        return e, 400
    return "Successfully Entered", 200



def get_teachers_detail():
    db, cursor, ret_code = dbconnect.conn()
    if ret_code != 200:
        return db, ret_code

    sql = 'SELECT TEACHERS_ID, TEACHERS_NAME, EMAIL_ID FROM teachers where VALID = 1'
    cursor.execute(sql)
    t_details = cursor.fetchall()
    
    if t_details == None or not len(t_details):
        return 'No teachers', 400
    return t_details, 200

def get_student_detail():
    db, cursor, ret_code = dbconnect.conn()
    if ret_code != 200:
        reurn db, ret_code

    sql = 'SELECT STUDENT_ID, STUDENT_NAME, EMAIL_ID FROM students WHERE VALID = 1'
    cursor.execute(sql)
    s_details = cursor.fetchall()

    if s_details == None or not len(s_details):
        return 'No students', 400
    return s_details, 200


def get_teacher_routine_detail(teacher_id):
    db, cursor, ret_code = dbconnect.conn()
    if ret_code != 200:
        return db, ret_code

    sql = 'SELECT TIME, DURATION, DESCRIPTION FROM routine_teacher where TEACHER_ID = %s AND MAIL = 0 AND DATE(TIME) = CURRENT_DATE + 1' %(teacher_id)
    cursor.execute(sql)
    routine_details = cursor.fetchall()

    if routine_details ==None or not len(routine_details):
        return 'No class', 400
    return routine_details, 200
    

def get_student_routine_detail(student_id):
    db, cursor, ret_code = dbconnect.conn()
    if ret_code != 200:
        return db, ret_code

    sql = 'SELECT SUBJECT_NAME, TEACHERS_NAME, TIME, DURATION, RS.DESCRIPTION FROM routine_student RS INNER JOIN routine_teacher RT ON RS.ROUTINE_TEACHER_ID = RT.ROUTINE_TEACHER_ID INNER JOIN subject s ON RT.SUBJECT_ID = s.SUBJECT_ID INNER JOIN teachers t ON t.TEACHERS_ID = RT.TEACHER_ID where RS.STUDENT_ID = %s AND DATE(TIME) = CURRENT_DATE + 1' %(student_id)
    cursor.execute(sql)
    routine_details = cursor.fetchall()

    if routine_details ==None or not len(routine_details):
        return 'No class', 400
    return routine_details, 200
