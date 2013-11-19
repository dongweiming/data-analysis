from data_analysis import db

class Apidist(db.Document):
    name = db.StringField(max_length=255, required=True)
    call = db.IntField(required=True)
    include = db.StringField(max_length=255, required=True)

class Celery(db.Document):
    cost = db.FloatField(required=True)
    time = db.DateTimeField(required=True)
    file = db.StringField(max_length=25, required=True)
    task = db.StringField(max_length=255, required=True)

class Mongo(db.Document):
    total = db.IntField(required=True)
    database = db.StringField(max_length=255, required=True)
    hour = db.DictField(required=True)
