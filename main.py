#!/usr/bin/python3
from flask import *
from flask_mail import Mail, Message
import modules.validate as validate
import modules.studentRegister as sR
import modules.get_db as get_db
import datetime

app = Flask(__name__)
app.secret_key = 'vivek'

mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME']= 'sinha22.sonam@gmail.com'
app.config['MAIL_PASSWORD'] = 'HaldiaInstitute'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success/')
def success():
    if 'user' in session:
        return render_template('login_success.html')
    return "you are logged out"

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
       user = request.form['nm']
       pwd = request.form['pwd']


       description, ret_code = validate.validateUser(user,pwd)
       
       if ret_code != 200:
           return (description),400
       
       session['user'] = user
       return redirect(url_for('success',name = user))
   
   else:
       user = request.args.get('nm')
       return redirect(url_for('success',name = user))


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
        print('Logout')
        return 'Logout'
    else:
        print('Already logged out')
        return 'Already logged out'



#SCHEDULE CLASS
@app.route('/schedule', methods = ['POST', 'GET'])
def schedule():
    if 'user' in session:
        if request.method == 'POST':
            #Getting input from HTML page
            subject_id = request.form['subject']
            teacher_id = request.form['teacher']
            students_id = request.form.getlist('stud')
            date = request.form['date']
            time = request.form['time']
            duration = request.form['duration']
            description_teacher = request.form['desc_teacher']
            description_student = request.form['desc_student']
            date1 = date +' '+ time
            
            #store it to db in loop
            msz, ret_code = get_db.insert_data(subject_id, teacher_id, students_id, date1, duration, description_teacher, description_student)
            #call send mail function
            #for student in student_id:
            #    get_db.get_student_detail
            if ret_code != 400:
                msg = Message('Hello', sender = 'sinha22.sonam@gmail.com', recipients = ['rishivivek1@gmail.com','sinha22.sonam@gmail.com'])
                msg.body = "Hello from Flask"
                mail.send(msg)
                return "Sent"



            #call send whatsapp message function

        subject = get_db.get_data('subject','SUBJECT_NAME, SUBJECT_ID')
        teacher = get_db.get_data('teachers','TEACHERS_NAME, TEACHERS_ID')
        student = get_db.get_data('students','STUDENT_NAME,STUDENT_ID')
        return render_template('Routine.html',subject = subject, teacher = teacher, student = student)
    else:
        return "Login to proceed"



#TEACHER INFORMATION LOAD IN TABLE
@app.route('/teacher', methods= ['POST', 'GET'])
def teacher():
    if 'user' in session:
        if request.method == 'POST':
            tname = request.form['tname']
            cno = request.form['cno']
            email = request.form['email']
            clas = request.form['class']
            subject = request.form['subject']

            description, ret_code = sR.teacherRegister(tname, cno, email, clas, subject)
            if ret_code !=200:
                return "Failure: Issue inserting data"
            return render_template('teacherLogin.html')
        return render_template('teacherLogin.html')
    else:
        return "Login to proceed"


#STUDENT INFORMATION LOAD IN TABLE
@app.route('/student',methods = ['POST', 'GET'])
def student():
    if 'user' in session: # and request.method == 'POST':
        if request.method == 'POST':
            # Getting inputs from HTML page
            sname = request.form['sname']
            whatsapp = request.form['whatsapp']
            fname = request.form['fname']
            fno = request.form['fno']
            email = request.form['email']
            clas = request.form['class']
            description , ret_code = sR.studentRegister(sname, whatsapp, fname, fno, email, clas)
            if ret_code != 200:
                return "Failure: Issue inserting data" 
            #return "Success: %s" % description
            return render_template('studentLogin.html')
        return render_template('studentLogin.html')

    else:
        return "Login to proceed"

#Send mail to Teacher
@app.route('/teacher_mail', methods = ['POST', 'GET'])
def teacher_mail():
    user = 'sinha22.sonam@gmail.com'
    dt = datetime.datetime.today().date() + datetime.timedelta(days = 1)
    t_detail, ret_code = get_db.get_teachers_detail()
    if ret_code !=200:
        for t in t_detail:
            t_id = t[0]
            t_name = t[1]
            t_email = t[2]
            msg = Message('Scheduled Class Details on '+dt ,sender = user ,  recipients = [user, t_email])
            msz = 'Hi ' + t_name + ', \n \n \t Below is the details of the class scheduled on ' + dt + '.\n'

            routine, ret_code = get_db.get_teacher_routine_detail(t_id)
            if ret_code != 200:
                for row in routine:
                    time = row[0]
                    duration = row[1]
                    desc = row[2]
                    
                    msz += 'At ' + time + ' for ' + duration + ' having description as ' + desc + '.\n'

                msz += '\n \n From, \n Unconve - '
                msg.body = msz
                mail.send(msg)
                return "Sent"
            else:
                return "No class"
        

#Send mail to Student
@app.route('/student_mail', methods = ['POST', 'GET'])
def student_mail():
    user = 'sinha22.sonam@gmail.com'
    dt = datetime.datetime.today().date() + datetime.timedelta(days = 1)
    s_detail, ret_code = get_db.get_student_detail()
    if ret_code != 200:
        for s in s_detail:
            s_id = s[0]
            s_name = s[1]
            s_email = s[2]
            msg = Message('Scheduled Class Details on ' +dt, sender = user, recipients = [user, s_email])
            msz = 'Hi ' + s_name + ', \n \n \t Below is the details of the class scheduled on '+ dt + '.\n'

            routine, ret_code = get_db.get_student_detail(s_id)
            if ret_code != 200:
                for row in routine:
                    subject = row[0]
                    teacher = row[1]
                    time = row[2]
                    duration = row[3]
                    desc = row[4]

                    msz += 'Subject: '+ subject + ' by ' + teacher + ' at ' + time + ' for '+ duration + ' having description as '+desc + '.\n'

                msz += '\n\n From, \n Unconve -'
                msg.body = msz
                mail.send(msg)
                return "Sent"
            else:
                return "No class"





if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 8443, debug = True)
