from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import user

class Show:
    db = "Belt2"
    def __init__(self,data):
        self.id=data["id"]
        self.user_id=data["user_id"]
        self.title=data["title"]
        self.network=data["network"]
        self.date=data["date"]
        self.description=data["description"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.skeptics= []


    @classmethod
    def save_new_show(cls, data):
        query ="INSERT INTO shows(user_id,title,network,date,description) VALUES (%(user_id)s, %(title)s,%(network)s,%(date)s,%(description)s)"
        print("testing save", query)
        return connectToMySQL(cls.db).query_db(query,data)
    

    @classmethod
    def get_all_shows(cls):
        query="SELECT * FROM shows"
        return connectToMySQL(cls.db).query_db(query)


    @classmethod
    def get_one(cls,show_id):
        data = {
            "id":show_id
        }
        query = "SELECT * FROM shows WHERE shows.id =%(id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])


    @classmethod
    def update_show(cls,data):
        query="UPDATE shows SET title =%(title)s, network =%(network)s, date=%(date)s,description=%(description)s WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query,data)
    


    @classmethod
    def destroy_show(cls,data):
        query = "DELETE FROM shows WHERE id =%(id)s"
        return connectToMySQL(cls.db).query_db(query,data)







    @staticmethod
    def validate_show(show):
        is_valid=True
        if len(show['title']) < 3:
            flash(("Name must be atleast 3 characters"))
            is_valid=False
        if len(show['network']) < 3:
            flash(("Network must be atleast 3 characters"))
            is_valid=False
        if len(show['description']) < 3:
            flash(("Description must be atleast 3 characters"))
            is_valid=False
        if not show['date']:
            flash("Please select a date")
            is_valid=False
        return is_valid