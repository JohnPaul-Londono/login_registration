from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
import re

class Users:
    def __init__( self, data ):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.confirm_password = data["confirm_password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def validate_user(user):
        email_reg = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        pw_reg = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')

        is_valid = True
        if len(user["first_name"]) <= 1:
            flash("First name must be at least 2 characters long.")
        if len(user["last_name"]) <= 1:
            flash("Last name must be at least 2 characters long.")
        if not email_reg.match(user["email"]):
            flash("Invalid Email")
            is_valid = False
        else:
            check_email = connectToMySQL("login_regis_scehma")
            query = "SELECT * FROM users WHERE email = %(email)s;"
            data = {
                "email":request.form["email"]
            }
            results = check_email.query_db(query, data)
            if results != ():
                flash ("Email already exists! Please use another one.")
                is_valid = False
        if not pw_reg.match(user["password"]):
            flash("Password must contain at least: one upper case letter, one lower case letter, one digit, one special character and 8 characters in length. ")
            is_valid = False
        if user["confirm_password"] != user["password"]:
            flash("Please make sure passwords match.")
            is_valid = False
        return is_valid

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, confirm_password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(confirm_password)s);"
        return connectToMySQL("login_regis_scehma").query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s"
        user_db = connectToMySQL("login_regis_scehma").query_db(query,data)

        if len(user_db) < 1:
            return False

        return cls(user_db[0])



    @classmethod
    def show_user(cls,data):
        query = "SELECT * FROM users  WHERE id =%(users_id)s "
        user_db = connectToMySQL("login_regis_scehma").query_db(query,data)
        return cls(user_db[0])
