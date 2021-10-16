from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    session,
    flash,
)
from functools import wraps
from init_db import get_db_connection

app = Flask(__name__)
app.config["SECRET_KEY"] = "APP"


# Check if user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        flash("You need to login.")
        return redirect(url_for("login"))
    return decorated_function


@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        username, password = request.form["username"], request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT password FROM users WHERE username=?", (username,)
        ).fetchone()
        conn.close()

        if user and password == user["password"]:
            session["username"] = username
            session["logged_in"] = True
            return redirect(url_for("main"))
        else:
            error = "Invalid Credentials. Please try again."
            flash(error)
            return redirect(request.url)

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("username", None)
    return redirect(url_for("login"))


# noinspection PyUnusedLocal
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.route("/")
@login_required
def main():
    return render_template("main.html")
