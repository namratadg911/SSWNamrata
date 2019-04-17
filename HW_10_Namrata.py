import unittest
from prettytable import PrettyTable
from collections import defaultdict
import os
import sqlite3

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
        self.remaining_required = set()
        self.remaining_electives = set()

    def add_course(self,course,grade):
        """if grades are less tha C return None"""
        grades = ['A','A-','B+','B','B-','C+','C']
        if grade in grades:
            self.completed_courses[course] = grade
        else:
            return None
        

    def info(self,major):
        remaining_required,remaining_electives = major.remain(self.completed_courses.keys())
        return [self.cwid,self.name,self.major,sorted(self.completed_courses.keys()),remaining_required,remaining_electives]
    
    @staticmethod
    def field():
        return ["CWID","Name","Major","Courses","Required","Electives"]


class Instructor:
    """Instructors details"""
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

class Major:
    

    def __init__(self):
        
        self.dept = ''
        self.remaining_required = set()
        self.remaining_electives = set()
    
    def remain(self,courses):
        """Calculating required and electives in student table"""
        if self.remaining_electives & courses:
            rem_electives = None
        else:
            rem_electives = sorted(self.remaining_electives)
        
        final_req = self.remaining_required - set(courses)

        return sorted(final_req), rem_electives
        
    def info(self):
        return [self.dept,sorted(self.remaining_required),sorted(self.remaining_electives)]
    
    @staticmethod
    def field():
        return ["Dept","Required","Electives"]
    
class Repository:

    def __init__(self,dir):
        self.students = dict()
        self.instructors = dict()
        self.majors = defaultdict(Major)
        
        self.add_Student(os.path.join(dir,"students.txt"))
        self.add_Instructor(os.path.join(dir,"instructors.txt"))
        self.add_grades(os.path.join(dir,"grades.txt"))
        self.add_majors(os.path.join(dir,"majors.txt"))
        
        self.student_pt()
        self.instructor_pt()
        self.majors_pt()
        self.instructor_db()

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

            
    def add_majors(self,path):
        
        for dept,flag,course in file_reader(path,3,'\t',False):
            self.majors[dept].dept = dept
            
            if flag == 'R':
                self.majors[dept].remaining_required.add(course)
            elif flag == 'E':
                self.majors[dept].remaining_electives.add(course)

        
    def student_pt(self):
        """PrettyTable for student,instructor and major"""
        pt = PrettyTable(field_names = Student.field())

        for s in self.students.values():
            pt.add_row(s.info(self.majors[s.major]))
        
        print(pt)

    def instructor_db(self):
        """Fetching data from sqlite """
        DB_File = "C:\\Users\\namra\\810.db"
        db = sqlite3.connect(DB_File)

        query = """SELECT i.CWID, i.Name, i.Dept, g.Course, count(*) as Total_students 
                            from HW11_instructors i join HW11_grades g on i.CWID = g.Instructor_CWID 
                            group by g.Course order by Total_students desc"""
        pt = PrettyTable(field_names=Instructor.field())
       
        for row in db.execute(query):
            pt.add_row(row)
        print(pt)
    

    def instructor_pt(self):
        pt = PrettyTable(field_names=Instructor.field())

        for i in self.instructors.values():
            for c in i.info():
                pt.add_row(c)
        
        print(pt)

    def majors_pt(self):
        pt = PrettyTable(field_names = Major.field())
        
        for major in self.majors.values():
            pt.add_row(major.info())
        print(pt)
        

class Report(unittest.TestCase):
    #Test student instructor and repository
    def test_Instructor(self):
        """Testcase for instructor"""
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
        """"Testcase for student"""
        student_val = [] 
        for s in Repository("C:\\Windows\\System32\\Files_namrata").students.values():
            student_val.append(s.info())

        self.assertEqual(student_val,[["10103","Baldwin, C","SFEN", ['CS 501','SSW 564','SSW 567','SSW 687'], {'SSW 555','SSW 540'},None],
                                                    ["10115","Wyatt, X","SFEN", ['CS 545','SSW 564','SSW 567','SSW 687'], {'SSW 555','SSW 540'},None],
                                                    ["10172","Forbes, I","SFEN", ['SSW 555','SSW 567'], {'SSW 564','SSW 540'}, {'CS 545','CS 501','CS 513'}],
                                                    ["10175","Erickson, D","SFEN", ['SSW 564','SSW 567','SSW 687'], {'SSW 555','SSW 540'}, {'CS 545','CS 501','CS 513'}],
                                                    ["10183","Chapman, O","SFEN", ['SSW 689'], {'SSW 567','SSW 555','SSW 564','SSW 540'}, {'CS 545','CS 501','CS 513'}],
                                                    ["11399","Cordova, I","SYEN", ['SSW 540'], {'SYS 612','SYS 800','SYS 671'},None],
                                                    ["11461","Wright, U","SYEN", ['SYS 611','SYS 750','SYS 800'], {'SYS 671','SYS 612'}, {'SSW 565','SSW 540','SSW 810'}],
                                                    ["11658","Kelly, P","SYEN", [], {'SYS 800','SYS 612','SYS 671'}, {'SSW 565','SSW 540','SSW 810'}],
                                                    ["11714","Morton, A","SYEN", ['SYS 611','SYS 645'], {'SYS 671','SYS 612','SYS 800'}, {'SSW 565','SSW 540','SSW 810'}],
                                                    ["11788","Fuller, E","SYEN", ['SSW 540'], {'SYS 671','SYS 612','SYS 800'},None]])

    
    def test_Major(self):
        """Testcase for major"""
        major_val = []

        for m in Repository("C:\\Windows\\System32\\Files_namrata").majors.values():
            major_val.append(m.info())
        
        self.assertEqual(major_val,[['SFEN',{'SSW 540', 'SSW 564', 'SSW 567', 'SSW 555'},{'CS 501', 'CS 513', 'CS 545'}],
                                    ['SYEN',{'SYS 671', 'SYS 612', 'SYS 800'},{'SSW 565', 'SSW 540', 'SSW 810'}]])



def main():
    print("in main")
    path = "C:\\Windows\\System32\\Files_namrata"
    rep = Repository(path)

if __name__ == '__main__':
    #unittest.main(exit=False, verbosity=2)
    main() 

