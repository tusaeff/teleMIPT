from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, request
import os
import psycopg2
from urllib.parse import urlparse

server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(server)


class Prepod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name


class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    prepod_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    def __init__(self, prepod_id, user_id):
        self.date = datetime.now()
        self.prepod_id = prepod_id
        self.user_id = user_id
