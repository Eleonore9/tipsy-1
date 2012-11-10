#!/usr/local/bin/python
# -*- coding=UTF-8 -*-
import os, sys
from flask import Flask, render_template, redirect, request, url_for, session, g
import model
app = Flask(__name__)


#connect to db before any request and disconnect afterwards
@app.before_request
def set_up_db():
    g.db = model.connect_db()

@app.teardown_request
def disconnect_db(e):
    g.db.close()
#------------------


# go to index and login views
@app.route("/")
def index():
    return render_template("index.html", user_name="chriszf")

@app.route("/login")
def login():
    return render_template("login.html")
#---------------------------------------


#authentification of the user and opening the session:
@app.route("/authenticate", methods=['POST'])
def authenticate():
    email = request.form['email']
    password = request.form['password']
    user = model.User.authenticate(g.db, email, password)
    session['user_id'] = user.id
    # flash('You were successfully logged in!')
    return redirect(url_for("list_tasks"))
#-----------------------------------------


#playing with the tasks:
@app.route("/tasks")
def list_tasks():
    user_id = session.get("user_id", None)
    user_obj = model.User.get_user(g.db, user_id)
    tasks_from_db = user_obj.get_tasks(g.db, user_id)
    return render_template("list_tasks.html", tasks=tasks_from_db)

@app.route("/save_task", methods=["POST"])
def save_task():
    title = request.form['title']
    user_id = session.get("user_id", None)
    print user_id
    model.Task.new(g.db, title, user_id)
    return redirect(url_for("list_tasks"))

#view for one particular task
@app.route("/task/<int:id>", methods=["GET"])
def view_task(id):
    task_from_db = model.Task.get_task(g.db, id)
    return render_template("view_task.html", task=task_from_db)

#mark this particular task as completed
@app.route("/task/<int:id>", methods=["POST"])
def complete_task(id):
    task = model.Task.get_task(g.db, id)
    task.complete_task(g.db, id)
    return redirect(url_for("list_tasks"))
#-----------------------------------------


#logout = close the session
@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect(url_for("index"))
#------------------------------------




app.secret_key="Ceci_n'est_pas_une_clef_secrète"





if __name__ == "__main__":
    app.run(debug=True)
