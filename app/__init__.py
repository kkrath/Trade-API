import os

import click
import json
from flask import Flask
from flask import request, Response, jsonify
from .models import Trade
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    

    db_url = os.environ.get("DATABASE_URL")

    if db_url is None:
        db_path = os.path.join(app.instance_path, "db.sqlite3")
        db_url = f"sqlite:///{db_path}"
        os.makedirs(app.instance_path, exist_ok=True)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    db.init_app(app)
    app.cli.add_command(init_db_command)

    return app


def init_db():
    db.drop_all()
    db.create_all()



@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")


#  @author kkrath ------ following code is written for the hacker rank test for salesforce ----------------
app = create_app()


# global variables
acceptable_types = ["buy", "sell"]
trade_collection = []
num = 0

# this is an auto incrementor function which returns continuous numbers on each call
def next_number():
    global num
    num += 1
    return num


# this will return a new trade object
def getNewTrade(data):
    id = next_number()
    type = data['type']
    user_id = data['user_id']
    symbol = data['symbol']
    shares  = data['shares']
    price  = data['price']
    timestamp  = data['timestamp']
    return Trade(id, type, user_id, symbol, shares, price, timestamp)


# this will do a binary search to fetch the trade by id
def searchTrade(id):
    l = 0
    h = len(trade_collection)
    m = l + (h - l) // 2
    while(l < h):
        if id == trade_collection[m].id:
            return trade_collection[m]
        elif id < trade_collection[m].id:
            h = m - 1
        else:
            l = m + 1
    return None


''' This section contains URI to resource mapping '''

# default URI will show home page with API documentation - swagger
@app.route('/')
def home():
    return "Work In progress !! Home Page will contain the API documentation soon."


# This URI will create trade for POST and Fetch all the trades for GET
# if the input does not meet the criteria it will throw 400
@app.route('/trades',  methods = ['POST','GET'])
def createTrade():
    if request.method == 'POST':
        new_trade = getNewTrade(request.get_json())
        # handling input validations
        if new_trade.shares not in range(1,100):
            return Response(status=400)
        elif new_trade.type not in acceptable_types:
            return Response(status=400)
        else:
            trade_collection.append(new_trade)
            return app.response_class(response=new_trade.toJson(),
                                  status=201,
                                  mimetype='application/json')
    elif request.method == 'GET':
            trades = [b.toString() for b in trade_collection]
            return app.response_class(response=json.dumps({"trades":trades}),
                                  status=200,
                                  mimetype='application/json')


# this URI will fetch the trade by id if it exists else throw 404
@app.route('/trades/<id>', methods = ['GET','DELETE', 'PUT', 'PATCH'])
def fetchTradeById(id):
    # we will do a binary search to fetch the trade as the trades are sorted by id
    if request.method == 'GET':
        result = searchTrade(int(id))
        if result:
            return app.response_class(response=result.toJson(),
                                  status=200,
                                  mimetype='application/json')
        else:
            return Response(status=404)
    else:
        return Response(status=405)
