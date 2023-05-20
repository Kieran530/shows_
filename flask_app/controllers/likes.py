from flask import render_template, request, redirect, session,flash
from flask_app.models.user import User
from flask_app.models.show import Show
from flask_app.models.like import Like
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/add_like/<int:show_id>', methods =['POST'])
def add_like(show_id):
    data ={
        "user_id":session['user_id'],
        "show_id":show_id
    }
    
    Like.add_like(data)
    return redirect("/shows")

@app.route("/unlike/<int:show_id>",methods = ['POST'])
def remove_like(show_id):
    data ={
        "user_id":session['user_id'],
        "show_id":show_id
    }
    Like.delete_like_from_user(data)
    return redirect("/shows")
