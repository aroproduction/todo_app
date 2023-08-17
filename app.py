from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


def readtodos():
    with open("static/todos.txt", "r") as t_rfile:
            t_data = t_rfile.readlines()
            t_col = []
            for i in t_data:
                t_d = i.split("|")
                t = t_d[0]
                d = t_d[1].split("\n")[0]
                col = [t, d]
                if col not in t_col:
                    t_col.append(col)
    return t_col


@app.route("/", methods=["GET", "POST"])
def todo_app():
    try:
        todo_title = request.form["title"]
        todo_desc = request.form["description"]
        with open("static/todos.txt", "a") as todo_file:
            todo_file.write(f"{todo_title}|{todo_desc}\n")
        return render_template("index.html", data=readtodos())
    except:
        return render_template("index.html", data=readtodos())


if __name__ == "__main__":
    app.run(debug=True)
