from flask import Flask, render_template, redirect, url_for, flash, session, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
import requests
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secreti hisfjidsjfiosdjfsjofsidjfoeapjdparfpa/sfk1233@e32dsds'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=4)

db = SQLAlchemy()
db.init_app(app)
