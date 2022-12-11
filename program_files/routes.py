from program_files import app, db, bcrypt, forms, TOKEN, functions
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from program_files.models import Games, User
from datetime import datetime, timedelta
import requests
from requests.exceptions import ConnectionError

secret_word = None
word_set = None
to_display = None
tries = None
blanks = None

@app.route("/")
def index():
    # print(current_user)
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            if current_user.is_authenticated:
                print(current_user)
            else:
                print("no current user")
            next_page = request.args.get("next")
            print("login successful")
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash("Login failure, please check details", "danger")
    return render_template("login.html", form=form, title="login")


@app.route("/register", methods=["GET", "POST"])
def register():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        encrypted_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            name=form.name.data, email=form.email.data, password=encrypted_password
        )
        db.session.add(user)
        db.session.commit()
        flash(f"User: {form.email.data} was successfully created, please log in")
        return redirect(url_for("login"))
    return render_template("register.html", form=form, title="register")



@app.route("/account_summary")
@login_required
def account_summary():
    name = current_user.name

    return render_template("summary.html", name=name)

@app.route("/game_lost")
@login_required
def game_lost():
    return render_template("game_lost.html")

@app.route("/game_won")
@login_required
def game_won():
    word = secret_word
    return render_template("game_won.html", word=word)


@app.route("/hangman")
@login_required
def hangman():
    name = current_user.name
    global secret_word
    global word_set
    global to_display
    global tries
    global blanks	
    secret_word = functions.get_random_word()
    word_set = "abcdefghijklmnopqrstuvwxyz"
    blanks = 0
    to_display = []
    for i,char in enumerate(secret_word):
        if char==" ":
            to_display.append(" ")
        else:
            to_display.append("_")
            blanks+=1
    tries = 0
    return render_template('hangman.html', name = name, to_display=to_display,word_set=word_set,tries="/static/img/hangman%d.png"%tries)

@app.route('/add_char',methods=["POST"])
def add_char():
    global secret_word
    global word_set
    global to_display
    global tries
    global blanks	

    letter = request.form["letter"]
	
    chance_lost = True
    for i,char in enumerate(secret_word):
        if char==letter:
            chance_lost = False
            to_display[i] = letter
            blanks-=1

    word_set = word_set.replace(letter,'')
    print("blanks",blanks)
    if chance_lost==True:
        tries += 1

        if tries==10:
            game_outcome = Games(
                game_outcome = "Lost",
                secret_word=secret_word,
                user_id=current_user.id
            )
            db.session.add(game_outcome)
            db.session.commit()
            return redirect('/game_lost')

    if blanks==0:
        game_outcome = Games(
                game_outcome = "Won",
                secret_word=secret_word,
                user_id=current_user.id
            )
        db.session.add(game_outcome)
        db.session.commit()
        return redirect('/game_won')

    return render_template('hangman.html',to_display=to_display,word_set=word_set,tries="/static/img/hangman%d.png"%tries)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
