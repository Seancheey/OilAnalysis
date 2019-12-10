from flask import Flask, render_template, request, flash, session, redirect
from BackEnd import *
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import DetachedInstanceError
from BackEnd.objects import OilNews
import random

import json
import plotly

import pandas as pd
import numpy as np

app = Flask(__name__)
news = None

def dummy_news():
    res = []
    for i in range(6):
        n = OilNews(news_id=0, title="news" + str(i + 1),
                    content="This is displaying because the news API is not working. No." + str(i + 1))
        res.append(n)
    return res


@app.route('/')
def homepage():
    # Grab the oil price data
    oil_prices = pd_get_oil_prices(1)

    # Definition of the graphs
    graphs = [
        dict(
            data=[
                dict(
                    x=oil_prices["price_time"],  # Can use the pandas data structures directly
                    y=oil_prices["price"]
                )
            ]
        )
    ]

    # Add "ids" to each of the graphs to pass up to the client for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    username = None
    global news
    news = get_oil_news_list()
    if len(news) < 3:
        news = dummy_news()
    for n in news[:3]:
        assert n.title
        assert n.author
        assert n.content
    if 'username' in session:
        username = session['username']
    twitters = ['WtiOil', 'CrudeOilBrokers', 'TullowOilplc', 'OilPriceHourly', 'OilPriceUpdate',
                'oilpricebot', 'oilandgasprice', 'theoilprice', 'OPIS', 'OilandEnergy']
    random.shuffle(twitters)
    return render_template('index.html', username=username, news=news[:9], ids=ids,
                           graphJSON=graphJSON, twitters=twitters)


@app.route('/login', methods=['POST'])
def login_handler():
    form = request.form
    # password is hashed on the client side
    email, password = form['email'], bytes.fromhex(form['password'])
    status = None
    try:
        status = login(email, password)
    except UserPasswordNoMatchError:
        flash("Password does not match in our database.")
    except UsernameDoNotExistsError:
        flash("The account does not exist in our database.")
    except EmailDoNotExistsError:
        flash("The account does not exist in our database.")
    except OperationalError:
        flash("System operational error. Cannot connect to Database: Connection refused")

    if status:
        session['username'] = email
        session['email'] = email
        session['token'] = status
    return redirect("/")


@app.route('/register', methods=['POST'])
def register_handler():
    form = request.form
    # password is hashed on the client side
    email, password, username = form['email'], bytes.fromhex(form['password']), form['username']
    try:
        register(username, password, email)
    except UserAlreadyExistsError:
        flash("This email has been registered. Please login using that email.")
    except EmailAlreadyExistsError:
        flash("This username has been taken by someone else.")
    except OperationalError:
        flash("System operational error. Cannot connect to Database: Connection refused")

    session['username'] = username
    session['email'] = email
    session['token'] = login(email, password)

    return redirect("/")


@app.route('/logout', methods=['POST'])
def logout_handler():
    session.clear()
    return redirect("/")


@app.route('/news/<int:news_id>')
def news_display(news_id):
    try:
        this_news = get_one_oil_news(news_id)
    except TypeError:
        return redirect('/')

    try:
        username = session['username']
    except KeyError:
        # User is not logged in
        username = None

    try:
        recom = random.sample(news[news_id:] + news[:news_id-1], 3)
    except TypeError:
        return redirect('/')

    return render_template('news.html', username=username, title=this_news.title,
                           author=this_news.author, data=this_news.publish_date,
                           content=this_news.content, ref=this_news.reference, recommendation=recom)


@app.route('/news/comments', methods=['POST'])
def submit_comment():
    form = request.form
    comment = form['comment']


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(host='0.0.0.0')
