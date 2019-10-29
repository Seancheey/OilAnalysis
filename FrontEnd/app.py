from flask import Flask, render_template, request, flash, session
from BackEnd.backend_api import *
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import DetachedInstanceError
from BackEnd.objects import OilNews

app = Flask(__name__)


def dummynews():
    res = []
    for i in range(6):
        n = OilNews(id=0, title="news"+str(i+1), content="This is displaying because the news API is not working. No."+str(i+1))
        res.append(n)
    return res

@app.route('/')
def homepage():
    username = None
    news = get_oil_news()
    if len(news) < 6:
        news = dummynews()
    try:
        for n in news[:3]:
            assert n.title
            assert n.author
            assert n.content
    except DetachedInstanceError:
        news = dummynews()
    if 'username' in session:
        username = session['username']
    return render_template('index.html', username=username, news=news[:12])


@app.route('/login', methods=['POST'])
def login_handler():
    form = request.form
    # password is hashed on the client side
    email, password = form['email'], str.encode(form['password'])
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
        session['username'] = email
        session['token'] = status
        return homepage()
    else:
        return render_template('index.html')


@app.route('/register', methods=['POST'])
def register_handler():
    form = request.form
    # password is hashed on the client side
    email, password, username = form['email'], str.encode(form['password']), form['username']
    status = None
    try:
        status = register(email, password, username)
    except UserAlreadyExistsError:
        flash("This email has been registered. Please login using that email.")
    except EmailAlreadyExistsError:
        flash("This username has been taken by someone else.")
    except OperationalError:
        flash("System operational error. Cannot connect to Database: Connection refused")

    if status:
        session['username'] = email
        session['token'] = status
        return homepage()
    else:
        return render_template('index.html')


@app.route('/logout', methods=['POST'])
def logout_handler():
    session.clear()
    return homepage()


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run()
