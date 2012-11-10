"""
model.py
"""
import sqlite3
import datetime, time

#now that we have classes, we don't need these gobal variables:
# TASK_COLS = ["id", "title", "created_at", "completed_at", "user_id"]
# USER_COLS = ["id", "email", "password", "username"]

def connect_db():
    return sqlite3.connect("tipsy.db")

def insert_into_table(db, table, columns, values):
    c = db.cursor()
    query_template = """INSERT INTO %s VALUES (%s)"""
    num_cols = len(columns)
    q_marks = ", ".join(["NULL"] + (["?"] * (num_cols-1)))
    query = query_template%(table, q_marks)
    res = c.execute(query, tuple(values))
    if res:
        db.commit()
        return res.lastrowid

def get_from_table_by_id(db, table_name, id):
    """Gets a dictionary out of the database given an id"""
    c = db.cursor()
    query_template = """SELECT * from %s WHERE id = ?"""
    query = query_template%(TABLE_NAME)
    c.execute(query, (id,))
    row = c.fetchone()
    if row:
        if TABLE_NAME == "Users":
            return make_user(row)
        elif TABLE_NAME == "Tasks":
            return make_task(row)
    return None



#--------------------We define our User class--------------------------------------

class User(object):
    #class attributes
    COLS = ["id", "email", "password", "username"]
    TABLE_NAME = "Users"

    #class instantiation and instance attributes
    def __init__(self, id, email, password, name):
        self.id = id
        self.email = email
        self.password = password
        self.name = name

    #class methods (related to the class User and not a specific user)
    @classmethod
    def new(cls, db, email, password, name):          
        vals = [email, password, name]
        return insert_into_table(db, cls.TABLE_NAME, cls.COLS, vals)

    @classmethod
    def authenticate(cls, db, email, password):
        c = db.cursor()
        query = """SELECT * FROM %s WHERE email=? AND password=?"""%(cls.TABLE_NAME)
        c.execute(query, (email, password))
        result = c.fetchone()
        if result:
            return cls(*result)
        return None

    @classmethod 
    def get_user(cls, db, user_id):
        """Creates an instance of the class User"""
        # get_from_table_by_id(db, cls.TABLE_NAME, user_id)
        # return cls(id=d_user["id"], email=d_user["email"], password=d_user["password"], name=d_user["username"])
        # the return statement is +/- the same as this: user = User(id, email, password, name)
        c = db.cursor()
        query = """SELECT * FROM %s WHERE id=?"""%(cls.TABLE_NAME)
        c.execute(query, (user_id,))
        row = c.fetchone()
        if row:
            return cls(*row)
        return None

    #instance method
    def get_tasks(self, db, user_id):
        """Get all the tasks matching the user_id, getting all the tasks 
        in the system if the user_id is not provided. Returns the results 
        as a list of dictionaries."""
        c = db.cursor()
        if self.id:
            query = """SELECT * from "Tasks" WHERE user_id = ?"""
            c.execute(query, (self.id,))
        else:
            query = """SELECT * from "Tasks" """
            c.execute(query)
        tasks = []
        rows = c.fetchall()
        for row in rows:
            task = dict(zip(Task.COLS, row))
            tasks.append(task)
        return tasks

    # def make_task(self, row):
    #     return dict(zip(self.COLS, row))

    # def make_user(self, row):
    #     d_user = dict(zip(self.COLS, row))
    #     return d_user


#--------------We define our class Task----------------------------------------------

class Task(object):

    #class attributes
    COLS = ["id", "title", "created_at", "completed_at", "user_id"]
    TABLE_NAME = "Tasks"

    #class instantiation and instance attributes
    def __init__(self, id, title, created_at, completed_at, user_id):
        self.id = id
        self.title = title
        self.created_at = created_at
        self.completed_at = completed_at
        self.user_id = user_id

    #class method 
    @classmethod
    # def new(cls, db, title, user_id = None):
    #     vals = [title, created_at, completed_at, user_id]
    #     return insert_into_table(db, cls.TABLE_NAME, cls.COLS, vals)
    def new(cls, db, title, user_id):
        now = datetime.datetime.now()
        vals = [title, now, None, user_id]
        return insert_into_table(db, cls.TABLE_NAME, cls.COLS, vals)

    @classmethod
    def get_task(cls, db, task_id):
        """Creates an instance of the class User"""
        c = db.cursor()
        query = """SELECT * FROM %s WHERE id=?"""%(cls.TABLE_NAME)
        c.execute(query, (task_id,))
        row = c.fetchone()
        if row:
            return cls(*row)
        return None

    #instance method
    def complete_task(self, db, task_id):
        """Mark the task with the given task_id as being complete."""
        c = db.cursor()
        now = datetime.datetime.now()
        query = """UPDATE %s SET completed_at=DATETIME('now') WHERE id=?"""%(self.TABLE_NAME)
        res = c.execute(query, (task_id,))
        if res:
            db.commit()
            return res.lastrowid
        else:
            return None

    

    