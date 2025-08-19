from website import *
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash

def login(username, password):
	check = User.query.filter_by(username=username).first()

	if check and check_password_hash(check.password, password):
		login_user(check)
		return 1

	else:
		return 0


def register(username, email, password):
	check = User.query.filter_by(username=username).first()

	if check:
		return 0

	new_user = User(
		username = username,
		email = email,
		password = generate_password_hash(password)
	)

	db.session.add(new_user)
	db.session.commit()

	return 1


def logout():
	logout_user()