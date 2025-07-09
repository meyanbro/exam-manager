class ForAdmin:
    def __init__(self,student,new_marks,subject):
        self.subject = subject
        self.student = student
        self.new_marks = new_marks

        self.prevMarks = self.student.obtained[self.subject][0]
    
    def approve(self,exam):
        th,practical_marks = self.student.obtained[self.subject]
        self.student.obtained[self.subject]= int(self.new_marks),int(practical_marks)

        exam.save()
    