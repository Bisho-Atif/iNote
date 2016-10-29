from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import config

App = Flask(__name__)
App.config.from_object(config)
db = SQLAlchemy(App)

from app import views
from app.models import models