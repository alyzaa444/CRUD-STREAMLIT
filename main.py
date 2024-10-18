# import libaries
import streamlit as st
import sqlite3



conn = sqlite3.connect('students.db')
c = conn.cursor()
c.execute(
    '''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL
    )'''
)
conn.commit()
class Student:
    def __init__(self,name,age,grade):
        self.name = name
        self.age = age
        self.grade = grade
        
    def add_student(self):
        c.execute('INSERT INTO students (name,age,grade) VALUES (?,?,?)', (self.name, self.age, self.grade))
        conn.commit()
    @staticmethod
    def get_all_students():
        c.execute('SELECT * FROM students')
        return c.fetchall()
    @staticmethod
    def update_student(student_id, new_name, new_age, new_grade):
        c.execute('UPDATE students SET name = ?, age = ?, grade = ? WHERE id = ?', (new_name, new_age, new_grade, student_id))
        conn.commit()
    @staticmethod
    def delete_student(student_id):
        c.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
st.title("Student Management System with SQLite Database")

st.header("Add Student")

name = st.text_input("Name")
age = st.number_input("Age", min_value=0, step=1)
grade = st.text_input("Grade")
if st.button("Add Student"):
    if name and age and grade:
        student = Student(name, age, grade)
        student.add_student()
        st.success(f"Student {name} added successfully!")
    else:
        st.error("Please provide complete details.")

# Read
st.header("All Students")
students = Student.get_all_students()
if students:
    for student in students:
        st.write(f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}, Grade: {student[3]}")
else:
    st.write("No students found.")
# Update
st.header("Update a Student")
student_id_to_update = st.number_input("Enter Student ID to Update", min_value=1, format="%d")
new_name = st.text_input("New Name", key="new_name")
new_age = st.number_input("New Age", min_value=1, key="new_age")
new_grade = st.selectbox("New Grade", ["A", "B", "C", "D", "E", "F"], key="new_grade")
if st.button("Update Student"):
    if new_name and new_age and new_grade:
        Student.update_student(student_id_to_update, new_name, new_age, new_grade)
        st.success(f"Student ID {student_id_to_update} updated successfully!")
    else:
        st.error("Please provide complete details for the update.")
# Delete
st.header("Delete a Student")
student_id_to_delete = st.number_input("Enter Student ID to Delete", min_value=1, format="%d", key="delete_id")
if st.button("Delete Student"):
    Student.delete_student(student_id_to_delete)
    st.success(f"Student ID {student_id_to_delete} deleted successfully!")
conn.close()