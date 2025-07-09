import pickle

def saveTheLargerStuff(CLASSES,SUBJECTS,TEACHERS,STUDENTS,fileToSave='BIGSTUFF.import'):
    toSave = open(fileToSave,'wb')
    pickle.dump([CLASSES,SUBJECTS,TEACHERS,STUDENTS],toSave)
    toSave.close()

def LoadTheLargerStuff(fileToSave='BIGSTUFF.import'):
    global CLASSES,SUBJECTS,TEACHERS,STUDENTS
    try:
        toLoad = open(fileToSave,'rb')
        BIGGER = pickle.load(toLoad)
        CLASSES = BIGGER[0]
        SUBJECTS = BIGGER[1]
        TEACHERS = BIGGER[2]
        STUDENTS = BIGGER[3]
        toLoad.close()
        # print(CLASSES)
    except:
        CLASSES = []
        SUBJECTS = []
        TEACHERS = []
        STUDENTS=[]

LoadTheLargerStuff()

class MainSystem:
    def load(file_name):
        file_name = open(file_name,"rb")

        stuff = (pickle.load(file_name))
        file_name.close()
        return stuff
    def __init__(self,test=True,d=None):
        self.test = test
        if test:
            self.term = "First Terminal Examination"
            self.title = None

            self.participatingClasses= CLASSES
            self.participatingSubjects = [[ParticipatingSubject(self,i,40,16,20,8) for i in range(len(SUBJECTS))] for i in CLASSES]
            self.participatingStudents = [ParticipatingStudent(i,self) for i in range(len(STUDENTS))]
            self.totalWorkingDays= 1034
            self.dateofIssue = "2024/07/01"
        else:
            self.documentFolder = d
            self.title = ""
            self.term = ""
            self.participatingClasses = []
            self.participatingStudents = []
            self.participatingSubjects = []
            self.totalWorkingDays = 0
            self.dateofIssue = 0
    
    def save(self):
        ''' change saving folder'''
        if not self.test:
          
            fileToWrite = None;fileToWrite2=None
            try:
                fileToWrite = open("exam.mey",'wb')
            except:
                print("TRYING NEXT")
            finally:
                try:
                    fileToWrite2 = open("exam.mey",'wb')
                except:
                    print("ERROR")
                    # showerror("Error","No such file Found\n\nYou are strongly advised to create a new Examination")
                    quit()
            
            for stds in self.participatingStudents:
                stds.pLabel = None
                stds.tLabel = None
            if fileToWrite:
                pickle.dump(self,fileToWrite)
                fileToWrite.close()
                print("WRITTEN IN NICE")
            if fileToWrite2:
                pickle.dump(self,fileToWrite2)
                fileToWrite2.close()
                print("WRITTEN IN both")
        

class ParticipatingSubject():
    def __init__(self,examination,index,full,pas,pracFull,pracPass):
        self.examination = examination
        self.index = index
        self.name = SUBJECTS[index]
        self.full = full
        self.pas = pas
        self.pracFull = pracFull
        self.pracPass = pracPass

class ParticipatingStudent():
    def __init__(self,index,examination,symbolNo='10',attend=10,classIndexGiven = None):
        self.examination = examination
        self.name = STUDENTS[index][0]
        if not classIndexGiven!=None:
            self.classIndex = STUDENTS[index][1]
        else:
            self.classIndex = classIndexGiven

        # self.classIndex = [i for i in range(len(examination.participatingSubjects)) if ]
        # print("index",self.classIndex)
        self.obtained = {i:[0,0] for i in examination.participatingSubjects[self.classIndex]}
        # print(self.obtained)
        self.attend = attend

        self.tLabel = None
        self.pLabel = None
        self.symbolNo = symbolNo