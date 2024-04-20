import sqlite3
from flask import Flask, render_template, request

conn = sqlite3.connect('run.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS info (
            student_id INTEGER PRIMARY KEY,
            name TEXT,
            class_id TEXT);
''')

cur.execute('''CREATE TABLE IF NOT EXISTS run (
            run_id INTEGER,
            student_id INTEGER,
            distance REAL,
            time REAL,
            date TEXT,
            PRIMARY KEY("run_id" AUTOINCREMENT)
            FOREIGN KEY("student_id") REFERENCES "info"("student_id"));
''')

conn.commit()
conn.close()

student_id = None
distance = None
name = None
class_id = None
time = None
date = None

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
  global student_id, name, class_id, distance, time, date
  if request.method == 'POST':
    student_id = int(request.form['student_id'])
    name = request.form['name']
    name = name.capitalize()
    class_id = request.form['class_id']
    distance = float(request.form['distance'])
    time = float(request.form['time'])
    date = request.form['date']
    conn = sqlite3.connect('run.db')
    cur = conn.cursor()
    cur.execute("SELECT count(*) studentCnt FROM info where student_id = " +
                str(student_id))
    count = cur.fetchall()[0][0]
    if count == 0:
      cur.execute(
          '''INSERT INTO info (student_id, name, class_id) VALUES (?,?,?)''',
          (student_id, name, class_id))

    cur.execute(
        '''INSERT INTO run (student_id, distance, time, date) VALUES (?,?,?,?)''',
        (student_id, distance, time, date))

    conn.commit()
    conn.close()

  conn = sqlite3.connect('run.db')
  cur = conn.cursor()
  cur.execute(
      '''SELECT i.student_id student_id, name, class_id, distance, time, date FROM info i, run r where i.student_id = r.student_id'''
  )
  rows = cur.fetchall()
  conn.close()
  return render_template('index.html',
                         rows=rows,
                         student_id=student_id,
                         name=name,
                         class_id=class_id,
                         distance=distance,
                         time=time,
                         date=date)


# @app.route('/search', methods=['GET', 'POST'])
# def search():
#   global student_id, name, class_id, distance, time, date
#   if request.method == 'POST':
#     student_id = request.form['student_id']
#     conn = sqlite3.connect('run.db')
#     cur = conn.cursor()
#     cur.execute("SELECT i.student_id student_id, name, class_id, distance, time, date FROM info i, run r where i.student_id = r.student_id and i.student_id = " + student_id)

#     rows = cur.fetchall()
#     conn.close()
#     return render_template('search.html', rows=rows, student_id=student_id, class_id=class_id, distance=distance, time=time, date=date)


@app.route('/search', methods=['GET', 'POST'])
def search():
  global student_id
  if request.method == 'POST':
    student_id = request.form['student_id']
    conn = sqlite3.connect('run.db')
    cur = conn.cursor()
    cur.execute("SELECT i.student_id studentid, name, class_id, distance, time, date FROM info i, run r where i.student_id = r.student_id and i.student_id = " + student_id)
    rows = cur.fetchall()
    conn.close()

    return render_template('search.html', rows=rows, student_id=student_id)
  else:
    return render_template('search.html')

@app.route('/leaderboard')
def leaderboard():
  conn = sqlite3.connect('run.db')
  cur = conn.cursor()
  cur.execute("SELECT i.student_id studentid, name, class_id, sum(distance) distance  FROM info i, run r where i.student_id = r.student_id group by studentid, name, class_id order by distance desc, name")
  rows = cur.fetchall()
  conn.close()
  return render_template('leaderboard.html', rows=rows)

@app.route('/tips')
def tips():
  return render_template('tips.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
