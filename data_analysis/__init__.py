from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "fetch_data"}
app.config["SECRET_KEY"] = "Keepssdf12q"

db = MongoEngine(app)
