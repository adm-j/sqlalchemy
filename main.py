from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, render_template, request
import sqlite3
import os.path

app = Flask(__name__)
list_of_files = []
base = declarative_base()
# engine = create_engine('sqlite:///:memory:', echo=True)


class User(base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    data = Column()

    def __repr__(self):
        return "<User(name = '%s', fullname = '%s', nickname='%s')>" % (self.name, self.fullname, self.nickname)


if os.path.isfile('./test_database.db'):
    select = sqlite3.connect('./test_database.db').cursor().execute("select * from data group by id")
    list_of_files = select.fetchall()
    sqlite3.connect('./test_database.db').close()


@app.route("/", methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        user_file = request.form['file']
        connection = sqlite3.connect('./test_database.db')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                            id integer PRIMARY KEY, content text NOT NULL);''')
        data_copy = cursor.execute("select count(*) from data")
        values = data_copy.fetchone()
        length = values[0] + 1
        rows = (length, user_file)
        list_of_files.append(rows)
        print(list_of_files)
        cursor.execute("INSERT INTO data VALUES (?, ?)", rows)
        connection.commit()
        connection.close()
        return render_template('template.html', file=list_of_files)
    else:
        return render_template('template.html', file=list_of_files)


if __name__ == '__main__':
    app.run(debug=True)
