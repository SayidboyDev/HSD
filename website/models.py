from datetime import datetime
from website import db
from flask_login import UserMixin

# Models
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    domeins = db.relationship('DomeinName', backref='user')

    def __str__(self):
        return self.username


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    published_date = db.Column(db.String(200), nullable=True, default=datetime.now)

    def __str__(self):
        return self.title


class Pricing(db.Model):
    __tablename__ = 'pricing'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    info = db.Column(db.String(200), nullable=False)

    def __str__(self):
        return self.title


class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    content = db.Column(db.String(200), nullable=False)

    def __str__(self):
        return f'{self.name}, {self.email}'


class DomeinName(db.Model):
	__tablename__ = 'domein_names'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(70), nullable=False, unique=True)
	price = db.Column(db.Integer, nullable=False) 
	dateowned = db.Column(db.String(200), default=datetime.now())
	subdomein_id = db.Column(db.Integer, db.ForeignKey('subdomeins.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	subdomein = db.relationship('Subdomein', backref='domeins') 

	def __str__(self):
		return self.name


class Subdomein(db.Model):
	__tablename__ = 'subdomeins'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(25), nullable=False, unique=True)
	price = db.Column(db.Integer, nullable=False)
	

	def __str__(self):
		return self.name


class HSBankAccount(db.Model):
    __tablename__ = 'HS_bank_accounts'
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(120))

    def __str__(self):
        return f'{self.id} : {self.type} - {self.account_number}'
