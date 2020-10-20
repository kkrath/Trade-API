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


# global variables
acceptable_types = ["buy", "sell"]
trade_collection = []
num = 0
# this is an auto incrementor function which returns continuous numbers on each call

def next_number():
    global num
    num += 1
    return num

@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")
    click.echo("Listening to http server")

app = create_app()

def getNewTrade(data):
    id = next_number()
    type = data['type']
    user_id = data['user_id']
    symbol = data['symbol']
    shares  = data['shares']
    price  = data['price']
    timestamp  = data['timestamp']
    return Trade(id, type, user_id, symbol, shares, price, timestamp)


@app.route('/')
def home():
    return "Invalid Request URL"

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
            return app.response_class(response=json.dumps(new_trade.toJson(), indent = 2),
                                  status=201,
                                  mimetype='application/json')
    elif request.method == 'GET':
            return app.response_class(response=json.dumps([b.toJson() for b in trade_collection], indent = 2),
                                  status=200,
                                  mimetype='application/json')


