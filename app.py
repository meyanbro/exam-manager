from flask import Flask,render_template,redirect,request,session,flash,url_for
import pickle
from datetime import timedelta
from artifacts import * 
from others import *
    
workingExamination = MainSystem.load("exam.mey")

participating_classes_names = [classes[0] for classes in workingExamination.participatingClasses]
app = Flask(__name__)
app.secret_key = "MEYAN"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)

app.jinja_env.globals.update(zip=zip)

all_passwords = { teachers[0].split()[0].lower() : ("abc",TEACHERS.index(teachers)) for teachers in TEACHERS}
toChange = []

for teacher in TEACHERS:
    print(teacher[0].lower())
    if teacher[0].lower().startswith('tek'):
        coordinator = TEACHERS.index(teacher)
        break
    else:
        print("NOT a  COORDINATOR")
       
else:
        quit()

@app.route('/admin_panel')
def admin_panel():
    if session['coord']:
        if request.method == "GET":
            return render_template("coord.html",mark_changes=toChange)
    else:
        redirect("/")

@app.route("/accept_change",methods=['POST'])
def accept_change():
    if session['coord']:
        id = request.form.get('change_id')

        toChange[int(id)].approve(workingExamination)
        toChange.pop(int(id))
    
        flash("Sucessfully Approved the Request",category="success")
        return redirect("/admin_panel")

@app.route("/reject_change",methods=['POST'])
def reject_change():
    if session['coord']:
        id = request.form.get('change_id')

        toChange.pop(int(id))
        flash("Sucessfully Disapproved the Request",category="warning")

        return redirect("/admin_panel")


@app.route("/update-symbol-numbers",methods=['POST'])
def symbol_update():
    for student_name, value in request.form.items():
        # Check if the form field is for theory or practical marks
        if student_name.startswith('new_symbol_no_'):

            current_student_name = student_name.replace("new_symbol_no_","")
            new_Symbol = request.form[student_name]
            
            print(current_student_name,new_Symbol)

            teacher_id = session['teacher_id']

    # getting the class
            for classes in workingExamination.participatingClasses:
                if classes[1] == teacher_id:
                    className = classes[0]
                    classIndex = workingExamination.participatingClasses.index(classes)
                    break

            students = []

            for stds in workingExamination.participatingStudents:
                if stds.classIndex == classIndex:
                    students.append(stds)
            
            # Find the specific student in your students list
            student = next((s for s in students if s.name == current_student_name), None)
            
            if student:
                student.symbolNo = new_Symbol
              
    
    # Perform any additional processing (e.g., save to database)
    try:
        # Example: Save marks to database
        workingExamination.save()
        
        # Redirect with success message
        print("DONE")
        flash('Symbol Numbers Updated successfully', 'success')
        return redirect(url_for('viewClass')+"#symbol")
    
    except Exception as e:
        # Handle any errors
        return 'error', e

@app.route('/change-marks',methods=['POST'])
def change_marks():
    for student_name, value in request.form.items():
        # Check if the form field is for theory or practical marks
        if student_name.startswith('marks_'):

            current_student_name = student_name.split("_")[1]
            theory_marks = request.form[student_name]
            
            print(current_student_name,theory_marks)

            teacher_id = session['teacher_id']

    # getting the class
            for classes in workingExamination.participatingClasses:
                if classes[1] == teacher_id:
                    className = classes[0]
                    classIndex = workingExamination.participatingClasses.index(classes)
                    break

            students = []

            for stds in workingExamination.participatingStudents:
                if stds.classIndex == classIndex:
                    students.append(stds)

            subName = student_name.split("_")[-1]

            all_subjects = workingExamination.participatingSubjects[classIndex]
            all_subjects_names = [sub.name for sub in all_subjects]

            if subName in all_subjects_names:
             # getting all the students infos
                selected_sub_obj = all_subjects[all_subjects_names.index(subName)]
            
            # Find the specific student in your students list
            student = next((s for s in students if s.name == current_student_name), None)
            
            print(student)
            if student and int(student.obtained[selected_sub_obj][0]) != int(theory_marks):
                # Update the student's marks for the current subject
                print(student.obtained[selected_sub_obj])
                for chagnes in toChange:
                    if chagnes.student == student and chagnes.subject == selected_sub_obj:
                        flash('This Student already has a pending request on the same subject', 'warning')
                        break
                else:
                    flash('Marks will be updated once the Exam Coordinator approves this', 'success')

                # th,practical_marks = student.obtained[selected_sub_obj]
                    toChange.append(ForAdmin(student,int(theory_marks),selected_sub_obj))
                # student.obtained[selected_sub_obj]= int(theory_marks),int(practical_marks)

                
        
            print("DONE")
    return redirect(url_for('viewClass')+"#target-selection")
    

@app.route('/logout')
def logout():
    session.clear()
    flash("Log out Successful",'success')
    return redirect('/')

@app.route('/submit-marks', methods=['POST'])
def submit_marks():
    for student_name, value in request.form.items():
        # Check if the form field is for theory or practical marks
        if student_name.startswith('theory_marks_'):

            current_student_name = student_name.replace('theory_marks_', '')
            theory_marks = request.form[student_name]
            
            # Find the corresponding practical marks
            practical_marks_key = f'practical_marks_{current_student_name}'
            practical_marks = request.form.get(practical_marks_key, 0)

            classIndex = session['class_index']
            subName = session['subject_name']
            all_subjects = workingExamination.participatingSubjects[classIndex]
            all_subjects_names = [sub.name for sub in all_subjects]

            if subName in all_subjects_names:
             # getting all the students infos
                selected_sub_obj = all_subjects[all_subjects_names.index(subName)]

            students = []
            for stds in workingExamination.participatingStudents:
                if stds.classIndex == classIndex:
                    students.append(stds)
            
            # Find the specific student in your students list
            student = next((s for s in students if s.name == current_student_name), None)
            
            if student:
                # Update the student's marks for the current subject
                print(student.obtained[selected_sub_obj])
                student.obtained[selected_sub_obj]= int(theory_marks),int(practical_marks)
              
    
    # Perform any additional processing (e.g., save to database)
    try:
        # Example: Save marks to database
        workingExamination.save()
        
        # Redirect with success message
        print("DONE")
        flash('Marks submitted successfully', 'success')
        return redirect(url_for('home'))
    
    except Exception as e:
        # Handle any errors
        return 'error', e

@app.route("/about-us")
def about_us():
    return render_template('about_us.html')

all_passwords = { teachers[0].split()[0].lower() : ("abc",TEACHERS.index(teachers)) for teachers in TEACHERS}

@app.route("/",methods=['GET','POST'])
def home():
    if request.method == "GET":
        if session.get('teacher_id') !=None:
            print(SUBJECTS)
            return render_template('index.html',subjects=SUBJECTS,classes = participating_classes_names,is_coord = session['coord'])
        else:
            return render_template('login.html')
    else:
        username= request.form['username']
        password = request.form['password']

        if all_passwords.get(username):

            if all_passwords.get(username)[0] == password:
                session['teacher_id'] = all_passwords.get(username)[1]

                # checking for coordinatoor
                for teacher in TEACHERS:
                    if teacher[0].lower().startswith(username):
                        if TEACHERS.index(teacher) == coordinator:
                            session['coord'] = True
                        else:
                            session['coord'] = False
                print(session['teacher_id'])
                flash("नमस्ते, "+TEACHERS[session['teacher_id']][0],category='warning')
                return redirect('/')
            else:
                flash("Incorrect Username or Password","info")
                return redirect('/')
        else:
            flash("Incorrect Username or Password","info")
            return redirect('/')

@app.route('/view-class')
def viewClass():
    
    teacher_id = session['teacher_id']
    print(teacher_id)
    # getting the class
    for classes in workingExamination.participatingClasses:
        if classes[1] == teacher_id:
            className = classes[0]
            classIndex = workingExamination.participatingClasses.index(classes)
            break
    else:
            flash("Your Class doesn't have an ongoing Exam",'info')
            return redirect('/')

    students = []

    for stds in workingExamination.participatingStudents:
        if stds.classIndex == classIndex:
            students.append(stds)
   
    # calculating failed students
    failed_stds = []
    total_gpa = 0
    for stds in students:
        for sub in workingExamination.participatingSubjects[classIndex]:
            if stds.obtained[sub][0] < sub.pas:
                failed_stds.append(stds)
                break

    # calculating percentages and gpa and ranks
    percentages_student = []
    for stds in students:
        percentages_student.append(calculatePercentage(stds,workingExamination.participatingSubjects[classIndex]))
    a= percentages_student.copy()
    b = percentages_student.copy()
    percentages_student.sort(reverse=True)
    
    ranks = []
    for elms in b:
        ranks.append(percentages_student.index(elms)+1)



    return render_template('view_class.html',subs=workingExamination.participatingSubjects[classIndex],failed_students=failed_stds,ranks=ranks,all_students=students,percentanges=a,total_students=len(students),class_name = className,pass_rate=round(100-(len(failed_stds)/len(students)*100),2))


def calculatePercentage(stud,workingSubjects):
    # for a stud with working subjects calculates the overall percentange:
    percentageList = []
    for workingSubject in workingSubjects:
        percentageList.append(((stud.obtained[workingSubject][0]+stud.obtained[workingSubject][1])/(workingSubject.full+workingSubject.pracFull))*100)
    return round(sum(percentageList)/len(percentageList),2)

@app.route('/process-selection', methods=['POST'])
def process_selection():
    selected_class = request.form.get("class")
    selected_subject = request.form.get("subject")

    # checking if the selected class has the selected subjects or not
    for classes in  workingExamination.participatingClasses:
        if classes[0] == selected_class:
            classIndex = workingExamination.participatingClasses.index(classes)
            break
    
    all_subjects = workingExamination.participatingSubjects[classIndex]
    all_subjects_names = [sub.name for sub in all_subjects]

    if selected_subject in all_subjects_names:
        # getting all the students infos
        selected_sub_obj = all_subjects[all_subjects_names.index(selected_subject)]
        all_students = []

        for stds in workingExamination.participatingStudents:
            if stds.classIndex == classIndex:
                all_students.append(stds)
        session['class_index'] = classIndex
        session['subject_name'] = selected_subject

        return render_template('submit.html',students = all_students,subject = selected_sub_obj)
    else:
        
        return render_template('error.html')

    
    

app.run()
