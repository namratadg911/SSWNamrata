import unittest
from prettytable import PrettyTable
from collections import defaultdict
import os


def file_reader(path, n, sep=",",header=True):
    """Check if the file is in correct format or not,"""
    #file_name = "C:\\Users\\namra\\Desktop\\hw08.txt"
    try: 
        fp = open(path, 'r')
    except FileNotFoundError:
        
        raise FileNotFoundError("Not found")
    else:
        with fp:
                for i, line in enumerate(fp):
                    fields = line.rstrip("\n").split(sep)
                    if len(fields) != n:
                        raise ValueError(f"ValueError: {path} has {len(fields)} fields on line {i+1} but expected {n}")
                    if header and i == 0:
                        continue
                    else:
                        yield fields

class Student:
    def __init__(self,cwid,name,major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.completed_courses = defaultdict(str)
    
    def add_course(self,course,grade):
        self.completed_courses[course]=grade

    def info(self):
        return[self.cwid,self.name,sorted(self.completed_courses.keys())]
    
    @staticmethod
    def field():
        return ["CWID","Name","Courses"]


class Instructor:
    def __init__(self, cwid, name, dept):
        self.cwid = cwid
        self.name = name
        self.dept = dept
        self.course = defaultdict(int) 

    def add_course(self,courses):
        self.course[courses] +=1
        
    def info(self):
        for course, students in self.course.items():
            yield[self.cwid,self.name,self.dept,course,students]

    @staticmethod
    def field():
        return ["CWID","Name","Dept","Courses","Students"]
           
class Repository:

    def __init__(self,dir):
        self.students = dict()
        self.instructors = dict()
        self.add_Student(os.path.join(dir,"students.txt"))
        self.add_Instructor(os.path.join(dir,"instructors.txt"))
        self.add_grades(os.path.join(dir,"grades.txt"))
        self.student_pt()
        self.instructor_pt()

    def add_Student(self, path):
        for cwid,name,major in file_reader(path,3,'\t',False):
            if cwid in self.students:
                print("Error")
            else:
                self.students[cwid] = Student(cwid,name,major)
    
    def add_Instructor(self,path):
        for cwid,name,dept in file_reader(path,3,'\t',False):
            if cwid in self.instructors:
                print("Error")
            else:
                self.instructors[cwid] = Instructor(cwid,name,dept)

    def add_grades(self,path):
        
        for scwid, course, grade, icwid in file_reader(path,4,'\t',False):
            self.students[scwid].add_course(course,grade)
            self.instructors[icwid].add_course(course)

    def student_pt(self):
        pt = PrettyTable(field_names=Student.field())

        for s in self.students.values():
            pt.add_row(s.info())
        
        print(pt)

    def instructor_pt(self):
        pt = PrettyTable(field_names=Instructor.field())

        for i in self.instructors.values():
            for c in i.info():
                pt.add_row(c)
        
        print(pt)

class Report(unittest.TestCase):
    #Test student instructor and repository
    def test_Instructor(self):
        inst_val = [] 
        for i in Repository("C:\\Windows\\System32\\Files_namrata").instructors.values():
            for row in i.info():
                inst_val.append(row)


        self.assertEqual(inst_val,[['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4],
                                    ['98765', 'Einstein, A', 'SFEN', 'SSW 540', 3],
                                    ['98764', 'Feynman, R', 'SFEN', 'SSW 564', 3],
                                    ['98764', 'Feynman, R', 'SFEN', 'SSW 687', 3],
                                    ['98764', 'Feynman, R', 'SFEN', 'CS 501', 1],
                                    ['98764', 'Feynman, R', 'SFEN', 'CS 545', 1],
                                    ['98763', 'Newton, I', 'SFEN', 'SSW 555', 1],
                                    ['98763', 'Newton, I', 'SFEN', 'SSW 689', 1],
                                    ['98760', 'Darwin, C', 'SYEN', 'SYS 750', 1],
                                    ['98760', 'Darwin, C', 'SYEN', 'SYS 611', 2],
                                    ['98760', 'Darwin, C', 'SYEN', 'SYS 800', 1],
                                    ['98760', 'Darwin, C', 'SYEN', 'SYS 645', 1]])
        
    def test_Student(self):
        student_val = [] 
        for s in Repository("C:\\Windows\\System32\\Files_namrata").students.values():
            student_val.append(s.info())

        self.assertEqual(student_val,[['10103','Baldwin, C',['CS 501', 'SSW 564', 'SSW 567', 'SSW 687']],
                    ['10115','Wyatt, X',['CS 545', 'SSW 564', 'SSW 567', 'SSW 687']],
                    ['10172','Forbes, I',['SSW 555', 'SSW 567']],
                    ['10175','Erickson, D',['SSW 564', 'SSW 567', 'SSW 687']],
                    ['10183','Chapman, O',['SSW 689']],
                    ['11399','Cordova, I',['SSW 540']],
                    ['11461','Wright, U',['SYS 611', 'SYS 750', 'SYS 800']],
                    ['11658','Kelly, P',['SSW 540']],
                    ['11714','Morton, A',['SYS 611', 'SYS 645']],
                    ['11788','Fuller, E',['SSW 540']] ])

if __name__ == '__main':
    unittest.main(exit=False, verbosity=2)

def main():
    path = "C:\\Windows\\System32\\Files_namrata"
    rep = Repository(path)

main() 

#calculated = {cwid:student.pt_row() for cwid,studnet in self.repo._studnts.items()}

#expected = ({cwid:[]})

#calculated = {tuple(detail) for instruct inn self.repo._instructors.values() for detail in instructor.pt_rows()}