import sqlite3 as sql
import time
import random
import string
import bcrypt

#salt = 'ao%(*#@)byiw45d98`/?.30pnw434983q0;$@02*(@57318h('.encode('utf-8')

def validatePassword(password):
    if len(password) > 7:
        if (any(c in string.digits) and 
            any(c in string.punctuation) and 
            any(c.isupper()) and
            any(c.uslower()) for c in password):

            return True
        
    return False

def insertUser(username, password, DoB):
    global salt
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM users WHERE username = '{username}'")
    if cur.fetchone() == None:
        if validatePassword(password):
            hashed = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt()).decode('utf-8')
            cur.execute(
                "INSERT INTO users (username,password,dateOfBirth) VALUES (?,?,?)",
                (username, hashed, DoB),
            )
    con.commit()
    con.close()


def retrieveUsers(username, password):
    global salt
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    hashedpass = cur.execute(f"SELECT password FROM users WHERE username = '{username}'")
    if cur.fetchone() == None:
        con.close()
        return False
    else:
        if bcrypt.checkpw(password.encode('utf-8'), hashedpass):
            with open("visitor_log.txt", "r") as file:
                number = int(file.read().strip())
                number += 1
            with open("visitor_log.txt", "w") as file:
                file.write(str(number))
            # Simulate response time of heavy app for testing purposes
            time.sleep(random.randint(80, 90) / 1000)
            con.close()
            return True
        else:
            con.close()
            return False


def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO feedback (feedback) VALUES ('{feedback}')")
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()
