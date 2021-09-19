from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from binance.client import Client


app = Flask(__name__)

app.config["SECRET_KEY"] = "4635fe7825ccfbd59785dc6a9d514442"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)

binance_client = Client("", "")


from application import routes, utils

db.drop_all()
db.create_all()
utils.load_transactions()
