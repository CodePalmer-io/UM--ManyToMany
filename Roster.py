import json
import sqlite3

conn = sqlite3.connect('rosterdb.sqlite')  # Created a database
cur = conn.cursor()  # 'File handler'

cur.executescript('''                               
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE user (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE course (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE
);

CREATE TABLE Member (
    user_id INTEGER,
    course_id INTEGER,
    role INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

fileName = input("Enter file name: ")  # Enter file name or fileName is 'roster-data.json'
if len(fileName) < 1:
    fileName = 'roster_data.json'

file_data = open(fileName)  # Opens the file
json_data = json.load(file_data)  # load the Json data and convert to a Python Dictionary

for entry in json_data:
    name = entry[0]
    title = entry[1]
    role_id = entry[2]

    #   print((name, title, role_id))                     # Testing with Print {name[0], title[1], role_id[2]}

    cur.execute('''INSERT OR IGNORE INTO User(name) VALUES (?)''', (name,))
    cur.execute('SELECT id FROM User WHERE name = ? ', (name,))
    user_id = cur.fetchone()[0]  # user_id retrieval

    cur.execute('''INSERT OR IGNORE INTO Course(title) VALUES (?) ''', (title,))
    cur.execute('SELECT id FROM Course WHERE title = ? ', (title,))
    course_id = cur.fetchone()[0]  # course_id retrieval

    cur.execute('''INSERT OR REPLACE INTO Member (user_id, course_id, role) VALUES (?, ?, ?)''',
                (user_id, course_id, role_id))
               # Replace to prevent duplicate -> updates info
conn.commit()  # Save changes

cur.execute('''
    SELECT 'XYZZY'|| hex(User.name || Course.title || Member.role) AS X FROM
    User JOIN Member JOIN Course
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X
''')
# Creates a new table that consists of the user.name, course.title, member.role ordered
result = cur.fetchone()
print("RESULT: " + str(result))
