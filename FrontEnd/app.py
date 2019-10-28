from flask import Flask, render_template, request, flash
from BackEnd.backend_api import *
from sqlalchemy.exc import OperationalError
app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login_handler():
    form = request.form
    # password is hashed on the client side
    email, password = form['email'], form['password']
    status = None
    try:
        status = login(email, password)
    except UserPasswordNoMatchError:
        flash("Password does not match in our database.")
    except UserDoNotExistsError:
        flash("The account does not exist in our database.")
    except OperationalError:
        flash("System operational error. Cannot connect to Database: Connection refused")

    # TODO - Also need username.
    if status:
        return render_template('index.html', token=status, username="User")
    else:
        return render_template('index.html')


@app.route('/register', methods=['POST'])
def register_handler():
    form = request.form
    # password is hashed on the client side
    email, password, username = form['email'], form['password'], form['username']
    status = None
    try:
        status = register(email, password, username)
    except UserAlreadyExistsError:
        flash("This email has been registered. Please login use that email.")
    except EmailAlreadyExistsError:
        flash("This username has been taken by someone else.")
    except OperationalError:
        flash("System operational error. Cannot connect to Database: Connection refused")

    if status:
        status = login(email, password)
        return render_template('index.html', token=status, username="User")
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run()
