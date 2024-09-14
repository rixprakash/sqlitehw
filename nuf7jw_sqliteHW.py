#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sqlite3
#creating the connection and the tables
connectionhw = sqlite3.connect('student_grades.db')
cursorhw = connectionhw.cursor()
cursorhw.execute('''
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
)
''')
cursorhw.execute('''
CREATE TABLE IF NOT EXISTS grades (
    grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject TEXT NOT NULL,
    grade INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
)
''')
connectionhw.commit()


# In[ ]:


#adding data into the tables
students_data = [
    ('Alice', 'Johnson'),
    ('Bob', 'Smith'),
    ('Carol', 'White'),
    ('David', 'Brown'),
    ('Eve', 'Davis')
]
cursorhw.executemany('''
INSERT INTO students (first_name, last_name) VALUES (?, ?)
''', students_data)
connectionhw.commit()
grades_data = [
    (1, 'Math', 95),
    (1, 'English', 88),
    (1, 'History', 90),
    (2, 'Math', 82),
    (2, 'English', 76),
    (2, 'History', 85),
    (3, 'Math', 90),
    (3, 'English', 91),
    (3, 'History', 88),
    (4, 'Math', 78),
    (4, 'English', 85),
    (4, 'History', 82),
    (5, 'Math', 88),
    (5, 'English', 79),
    (5, 'History', 84)
]
cursorhw.executemany('''
INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)
''', grades_data)
connectionhw.commit()


# In[ ]:


#join data to view all students name and grades
cursorhw.execute('''
SELECT students.first_name, students.last_name, grades.subject, grades.grade
FROM students
JOIN grades ON students.student_id = grades.student_id
''')
joined_datahw = cursorhw.fetchall()
print("Joined students and grades details:")
for row in joined_datahw:
    print(row)


# In[ ]:


#avg grade for students
cursorhw.execute('''
SELECT students.first_name, students.last_name, AVG(grades.grade) as average_grade
FROM students
JOIN grades ON students.student_id = grades.student_id
GROUP BY students.student_id
''')
avggrades = cursorhw.fetchall()
for row in avggrades:
    print(row)


# In[ ]:


#students with highest avg
cursorhw.execute('''
SELECT students.first_name, students.last_name, AVG(grades.grade) as average_grade
FROM students
JOIN grades ON students.student_id = grades.student_id
GROUP BY students.student_id
ORDER BY average_grade DESC
LIMIT 1
''')
highestavggrade = cursorhw.fetchone()[0]
print(f"The student with the highest average grade is: {highestavggrade}")


# In[ ]:


#avg grade for math 
cursorhw.execute('''
SELECT AVG(grade) as average_math_grade
FROM grades
WHERE subject = 'Math'
''')
mathavggrade = cursorhw.fetchone()[0]
print(f"The average grade for the math subject is: {mathavggrade}")


# In[ ]:


#students with 90 or higher
cursorhw.execute('''
SELECT DISTINCT students.first_name, students.last_name
FROM students
JOIN grades ON students.student_id = grades.student_id
WHERE grades.grade > 90
''')
gradesabove90 = cursorhw.fetchall()
connectionhw.close()
for row in gradesabove90:
    print(row)


# In[ ]:


#pandas for dataframes
import pandas as pd
students_df = pd.read_sql_query('SELECT * FROM students', connectionhw)
grades_df = pd.read_sql_query('SELECT * FROM grades', connectionhw)
print(students_df)
print(grades_df)


# In[ ]:


#joint data
joined = '''
SELECT students.first_name, students.last_name, grades.subject, grades.grade
FROM students
JOIN grades ON students.student_id = grades.student_id
'''
joined_df = pd.read_sql_query(joined, connectionhw)
print(joined_df)


# In[ ]:


#plot avg grades for each student
import matplotlib.pyplot as plt
avg_grades_df = joined_df.groupby(['first_name', 'last_name'])['grade'].mean().reset_index()
avg_grades_df.columns = ['First Name', 'Last Name', 'Average Grade']
plt.figure(figsize=(10, 6))
plt.bar(avg_grades_df['First Name'] + ' ' + avg_grades_df['Last Name'], avg_grades_df['Average Grade'], color='lightblue')
plt.xlabel('Student')
plt.ylabel('Average Grade')
plt.title('Average Grades for Each Student')
plt.xticks(rotation=45)
plt.show()


# In[ ]:


#avg grade for each subject 
import matplotlib.pyplot as plt
avg_subject_grades_df = joined_df.groupby('subject')['grade'].mean().reset_index()
avg_subject_grades_df.columns = ['Subject', 'Average Grade']
plt.figure(figsize=(10, 6))
plt.bar(avg_subject_grades_df['Subject'], avg_subject_grades_df['Average Grade'], color='lightgreen')
plt.xlabel('Subject')
plt.ylabel('Average Grade')
plt.title('Average Grade for Each Subject')
plt.xticks(rotation=45)
plt.show()


# In[ ]:


#bonus task 
#student with highest grades in each subject
import pandas as pd
import sqlite3
cursorhw.execute('''
SELECT grades.subject, students.first_name || ' ' || students.last_name AS student_name, MAX(grades.grade) AS highest_grade
FROM grades 
JOIN students ON grades.student_id = students.student_id
GROUP BY grades.subject
''')
highestgradestudents = cursorhw.fetchall()
for row in highestgradestudents:
    print(row)


# In[ ]:


#bonus task
#visual results in bar chart: THIS CODE DOES NOT WORK -> trying to make the color of bars as the students but i am not sure how to do that
dfcolumns = ['subject', 'student_name', 'highest_grade']
highest_grades_df = pd.DataFrame(highestgradestudents, columns=dfcolumns)
plt.figure(figsize=(10, 6))
plt.bar(highest_grades_df['subject'], highest_grades_df['highest_grade'], color= highest_grades_df['student_name']))
plt.xlabel('Subject')
plt.ylabel('Highest Grade')
plt.title('The Student with the Highest Grade for Each Subject')
plt.xticks(rotation=45)
plt.show()

