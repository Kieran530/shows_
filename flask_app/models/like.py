from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import user
from flask_app.models import show

class Like:
    db="Belt2"
    def __init__(self,data):
        self.id=data["id"]
        self.user_id=data["user_id"]
        self.show_id=data["show_id"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.user=None

    @classmethod
    def add_like(cls,data):
        query="INSERT INTO likes(user_id,show_id) VALUES (%(user_id)s,%(show_id)s)"
        print("testing add like",query)
        return connectToMySQL(cls.db).query_db(query,data)


    @classmethod
    def get_all_users_likes_for_show(cls,data):
        query= "SELECT * FROM likes JOIN users on users.id= likes.user_id WHERE likes.show_id =%(id)s"
        results=connectToMySQL(cls.db).query_db(query,data)
        all_likers=[]
        for row_from_db in results:
            one_liker=cls(row_from_db)
            one_liker_user_info ={
                "id":row_from_db['users.id'],
                "first_name":row_from_db['first_name'],
                "last_name":row_from_db['last_name'],
                "email":row_from_db['email'],
                "password":row_from_db['password'],
                "created_at":row_from_db['created_at'],
                "updated_at":row_from_db['updated_at']
            }
            like_person=user.User(one_liker_user_info)
            one_liker.user=like_person
            all_likers.append(one_liker)
        return all_likers
    
    @classmethod
    def get_like_count_for_show(cls, data):
        query = "SELECT COUNT(*) AS like_count FROM likes WHERE show_id = %(id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        like_count = result[0]['like_count'] if result else 0
        return like_count

    @classmethod
    def delete_like_from_user(cls,data):
        query="DELETE FROM likes where likes.user_id = %(user_id)s AND likes.show_id =%(show_id)s"
        return connectToMySQL(cls.db).query_db(query,data)
    

    @classmethod
    def get_likes_from_current_user(cls, user_id):
        query = "SELECT * FROM likes JOIN users ON likes.user_id = users.id WHERE likes.user_id = %(user_id)s"
        data = {'user_id': user_id}
        results= connectToMySQL(cls.db).query_db(query, data)
        return [result['show_id']for result in results]