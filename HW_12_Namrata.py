from flask import Flask, render_template
import sqlite3

app = Flask(__name__, template_folder='templates')

@app.route('/details')
def instructor_demo():
    """Query for instructor summary"""
    DB_File = "C:\\Users\\namra\\810.db"

    query = """SELECT i.CWID, i.Name, i.Dept, g.Course, count(*) as Total_students 
                                from HW11_instructors i join HW11_grades g on i.CWID = g.Instructor_CWID 
                                group by g.Course order by Total_students desc"""

    db = sqlite3.connect(DB_File)
    rows = db.execute(query)

    data = [{'CWID':CWID,'Name':Name,'Department':Dept,'Courses':Course,'Total_students':Total_students}
            for CWID, Name, Dept, Course, Total_students in rows]

    db.close()
# To combine base.html and parameters.html from python program to display html document"""  
    return render_template('parameters.html',
                            title="Stevens Repository", 
                            table_title ="Number of students by course and instructor",
                            instructors=data)

app.run(debug=True)