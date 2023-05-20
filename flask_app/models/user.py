from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    db = "Belt2"
    def __init__(self,data):
        self.id=data["id"]
        self.first_name=data["first_name"]
        self.last_name=data["last_name"]
        self.email=data["email"]
        self.password=data["password"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        


    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s, %(email)s,%(password)s,NOW(), NOW());"
        print("checking save query",query)
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_email(cls,data):
        query =' SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query =' SELECT * FROM users WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_one(cls,user_email):
        data = {
            "email": user_email
        }
        sql = "SELECT * FROM users WHERE email=%(email)s"
        results = connectToMySQL(cls.db).query_db(sql, data)
        return cls(results[0])




    @staticmethod
    def validate_user(user):
        is_valid=True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results= connectToMySQL(User.db).query_db(query,user)
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters", "register")
            is_valid=False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters","register")
            is_valid=False
        if len(user['password']) < 6:
            flash("Password must be at least 6 characters","register")
            is_valid=False
        if len(results)>=1:
            flash("Email already taken.","register")
            is_valid=False
        if not any(char.isupper() for char in user['password']):
            flash("Password must contain at least one uppercase letter", "register")
            is_valid = False
        if not any(char.isdigit() for char in user['password']):
            flash("Password must contain atleast one number","register")
            is_valid = False

        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "register")
            is_valid = False
        if (user['confirm_password']) != user['password']:
            flash("password does not match", "register")
            is_valid=False
        return is_valid