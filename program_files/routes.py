from program_files import app, db, bcrypt, forms, TOKEN
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from program_files.models import Transaction, User
from datetime import datetime, timedelta
import requests
from requests.exceptions import ConnectionError


@app.route("/")
def index():
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
    names = User.query.filter_by(id=current_user.id).all()
    name = names[0]
    print(type(name))


    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    cash_balance = sum([transaction.transaction_amount for transaction in transactions])
    all_stock_names = set(
        [
            transaction.stock_name
            for transaction in transactions
            if transaction.stock_name is not None
        ]
    )
    stocks = {}
    for stock in all_stock_names:
        stock_quantity = sum(
            [
                transaction.stock_quantity
                for transaction in transactions
                if transaction.stock_name == stock
            ]
        )
        if stock_quantity != 0:
            stocks[stock] = stock_quantity
    return render_template("summary.html", cash_balance=cash_balance, stocks=stocks, name=name)





@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
