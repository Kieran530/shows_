from flask import render_template, request, redirect, session,flash,url_for
from flask_app.models.user import User
from flask_app.models.show import Show
from flask_app.models.like import Like
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/shows")
def main_screen():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    data ={
        "id":session['user_id']
    }
    current_user = session['user_id']
    
    user_id=session['user_id']
    all_shows=Show.get_all_shows()
    
    
    liked_shows = Like.get_likes_from_current_user(user_id)

    return render_template("/main.html",liked_shows=liked_shows,user=User.get_by_id(data),current_user=current_user, all_shows=all_shows)








@app.route("/shows/new")
def display_show_form():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    return render_template("add_new.html")

@app.route("/create", methods = ['POST'])
def create_new_show():
    if not Show.validate_show(request.form):
        return redirect("/shows/new")

    data = {
        "user_id":session['user_id'], 
        "title":request.form['title'],
        "network":request.form['network'],
        "date":request.form['date'],
        "description":request.form['description'],
    }

    Show.save_new_show(data)
    return redirect('/shows')

@app.route("/shows/<int:show_id>")
def display_show_info(show_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    current_show=Show.get_one(show_id)
    data={
        "id":session['user_id']
    }
    
    data2 ={
        "id":current_show.user_id
    }


    user_poster=User.get_by_id(data2)
    data3={
        "id":show_id
    }

    likes_count= Like.get_like_count_for_show(data3)
    return render_template("show.html",likes_count=likes_count,user=User.get_by_id(data),current_show=current_show, user_poster=user_poster)

@app.route('/shows/edit/<int:show_id>')
def display_edit_show(show_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    data ={
        "id":session['user_id']
    }
    current_show=Show.get_one(show_id)

    return render_template("edit.html",current_show=current_show,user=User.get_by_id(data))

@app.route('/shows/edit/<int:show_id>', methods =['POST'])
def update_show_info(show_id):
    if not Show.validate_show(request.form):
        return redirect(f"/shows/edit/{show_id}")

    data = {
        "id":show_id, 
        "title":request.form['title'],
        "network":request.form['network'],
        "date":request.form['date'],
        "description":request.form['description'],
    }

    Show.update_show(data)
    return redirect('/shows')

@app.route("/delete/<int:show_id>")
def delete_show(show_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    data ={
        "id":show_id
    }
    
    Show.destroy_show(data)
    return redirect('/shows')