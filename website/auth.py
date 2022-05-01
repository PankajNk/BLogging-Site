# this is seperate file that contain relatedto authotion like logon login out

from flask import Blueprint,render_template, redirect, url_for,request,flash
#request contains all data of post and get
from . import db
from .models import User

from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth= Blueprint("auth",__name__)

@auth.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password): #user.password is hash password
                flash('logged in', category='success')
                login_user(user, remember=True) #tis holds the current session info
                return redirect(url_for('views.home'))
            else:
                flash('Password incorrect ', category='error')
        else:
            flash('Email does not exist ', category= 'error')




    return render_template("login.html", user=current_user)

@auth.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get("email") # emailis name fromloginor signup page---- get not to crash if  NULL return the null
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exist = User.query.filter_by(email=email).first()
        username_exist = User.query.filter_by(username=username).first()
        if email_exist:
            flash('Email already exist', category='error')
        elif username_exist:
            flash('Username alrready exist',category='error')
        elif password1 != password2:
            flash('Password dont match',category='error')
        elif len(username)< 2:
            flash('username too short', category='error')
        elif len(password1) < 4:
            flash('password too short')
        elif len(email) <4:
            flash('Invalid email')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('user created')
            return redirect(url_for('views.home'))




    return render_template("signup.html", user=current_user)

@auth.route("/logout")
@login_required   #this gives only acess when  login-user-is -used
def logout():
    #return render_template("logout.html")
    logout_user()
    return redirect(url_for("views.home")) #home is function name in viwes