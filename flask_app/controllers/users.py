from flask import Flask,render_template,redirect,request,session,flash
from flask_app import app
from flask_app.models.user import Users
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route ("/")
def index():
    return render_template("login_regis.html")

@app.route("/register", methods=["POST"])
def validate_user():
    if Users.validate_user(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        pw_hash = bcrypt.generate_password_hash(request.form["confirm_password"])
        data = {
            "first_name":request.form["first_name"],
            "last_name":request.form["last_name"],
            "email":request.form["email"],
            "password":pw_hash,
            "confirm_password":pw_hash,
        }

        users_id = Users.save(data)
        session["users_id"] = users_id
        # flash("User created!")
        return redirect("/dashboard")
    else:
        return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    data ={
        "email":request.form["email"]
    }
    user_in_db = Users.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password,request.form["password"]):
        flash("Invalid Email/Password")
        return redirect("/")

    session["users_id"] = user_in_db.id
    return redirect("/dashboard")



@app.route("/dashboard")
def dashboard():
    if "users_id" not in session: #protect, this must be in the exam
        flash("Must be logged in!")
        return redirect("/")
    else:
        data = {
            "users_id":session["users_id"]
        }
        users = Users.show_user(data)
        return render_template("success.html", users=users)

@app.route("/logout")
def logout():
    session.clear()
    flash("logged out!")
    return redirect("/")