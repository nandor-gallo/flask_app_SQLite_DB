from flask import Flask

from flask import *
import sqlite3 as sql
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/show', methods=['POST', 'DELETE'])
def show():
    if request.method == 'POST':
        print("POST")
        SID = request.form['SID']
        Fname = request.form['Fname']
        Lname = request.form['Lname']
        birthday = request.form['birthday']
        amountDue = request.form['amount']

        with sql.connect("database.db") as con:
            print("DATABASE OPEN")
            cur = con.cursor()
            cur.execute("SELECT rowid FROM students WHERE sid = ?", (SID,))
            data = cur.fetchall()
            if request.form['action'] == 'Send':

                print("SENDING")
                if len(data) == 0:
                    cur.execute(
                        "INSERT INTO students(sid, first, last, dob, amount) VALUES(?, ?, ?, ?, ?)", (SID, Fname, Lname, birthday, amountDue))
                    con.commit()
                    msg = "Successfully added to db"
                else:
                    # If SID in DB then update the values of the SID
                    con.execute(
                        "UPDATE students set first = ?, last = ?, dob = ?, amount = ? where sid = ?", (Fname, Lname, birthday, amountDue, SID,))
                    con.commit()
                    msg = "Successfully updated db"
            elif request.form['action'] == 'Delete':
                msg = "Successfully deleted from db"
                cur.execute("DELETE from students where sid = ?", (SID,))
                con.commit()
                print("DELETEING")
    return render_template("results.html", msg=msg)


@app.route('/list')
def list():
    print("LIST LOADING")
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall()
    return render_template("list.html", rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
