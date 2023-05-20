from flask import render_template, request, redirect, session,flash
from flask_app.models.user import User
from flask_app.models.show import Show
from flask_app.models.like import Like
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    form_data=session.pop("form_data",None)
    return render_template("login&reg.html", form_data=form_data)

@app.route("/register", methods = ['POST'])
def register():
    if not User.validate_user(request.form):
            session['form_data']=request.form
            return redirect('/')

    data ={
        "first_name":request.form['first_name'],
        "last_name":request.form['last_name'],
        "email":request.form['email'],
        "password":bcrypt.generate_password_hash(request.form['password'])
        }
    id=User.save(data)
    print("testing id",id)
    session['user_id']=id
    print("checking request form",request.form)
    
    return redirect("/shows")


@app.route("/login", methods = ["POST"])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email", "login")
        return redirect('/')
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash ("invalid password","login")
        return redirect('/')
    session['user_id']=user.id
    return redirect('/shows')



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")