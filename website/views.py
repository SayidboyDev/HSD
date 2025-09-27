from website import *
from .models import *
from .auth import login, logout, register
from flask_login import LoginManager, login_required, current_user, login_user, logout_user

# Login manager 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_func'


bank_api = 'http://127.0.0.1:2020/'


@login_manager.user_loader
def user_load(id):
	return User.query.get(int(id))


@app.route('/')
@app.route('/home')
def home():
	services = Service.query.all()
	return render_template('index.html', services=services)


@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/services')
def services():
	services = Service.query.all()
	return render_template('services.html', services=services)


@app.route('/domein/sell', methods=['POST', 'GET'])
@login_required
def domein_selling():
	subdomeins = Subdomein.query.all()
	domeins = DomeinName.query.all()

	if request.method == 'POST':
		domein_name = request.form.get('domein_name')
		subdomein = request.form.get('subdomein')
		
		if not domein_name or not subdomein:
			flash('Input cant\'t be empty!')
			return redirect(url_for('domein_selling'))

		subdomein = Subdomein.query.filter_by(name=subdomein).first()
		if not subdomein or subdomein == 'all':
			result = {}
			for s in subdomeins:
				check = DomeinName.query.filter_by(name = domein_name+s.name, subdomein_id = s.id).first()
				if not check:
					result[domein_name+s.name] = {'type': 'available', 'price': s.price, 'domein_name': domein_name+s.name, 'subdomein_id': s.id}
				if check:
					result[domein_name+s.name] = {'type': 'not available', 'owner_id': check.user_id}
			return render_template('domein_selling.html', subdomeins=subdomeins, result=result, list=True)

		check = DomeinName.query.filter_by(name = domein_name+subdomein.name, subdomein_id = subdomein.id).first()

		if check:
			result = {'domein_name': f'{domein_name}{subdomein}',
						'type': 'not available',
						'owner_id': check.user_id
					}
		elif not check:
			result = {'domein_name': f'{domein_name}',
					'subdomein_id': f'{subdomein.id}',
					'subdomein': subdomein.name, 
					'type': 'available',
					'price': subdomein.price
					}
		else:
			return 0
			
		return render_template('domein_selling.html', subdomeins=subdomeins, result=result)

	return render_template('domein_selling.html', subdomeins=subdomeins)


@app.route('/pricing')
def pricing(show_lower: bool=None):
	pricing = Pricing.query.all()
	if show_lower:
		return render_template('low_pricing.html')
	return render_template('pricing.html', pricing=pricing)


@app.route('/login', methods=['POST', 'GET'])
def login_func():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')

		res = login(username, password)
		if not res:
			flash('Noto\'g\'ri username yoki parol!')
			return redirect(url_for('login_func'))
		flash('Successfully login!')
		return redirect(url_for('home'))

	return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register_func():
	if request.method == 'POST':
		username = request.form.get('username')
		email = request.form.get('email')
		password = request.form.get('password')

		res = register(username, email, password)

		if not res:
			flash('User allaqachon mavjud!')
			return redirect(url_for('register_func'))
		flash('Successfully registerd!')
		return redirect(url_for('login_func'))

	return render_template('register.html')


@app.route('/logout')
def logout_func():
	logout()
	return redirect(url_for('login_func'))


@app.route('/profile')
def profile():
	user = User.query.filter_by(id = current_user.id)
	chats = Chat.query.filter(Chat.first_member_id == current_user.id or Chat.second_member_id == current_user.id).all()

	return render_template('profile.html', user=user, chats=chats)

@app.route('/profile/chats')
def profile_chats():
	chats = Chat.query.filter(Chat.first_member_id == current_user.id or Chat.second_member_id == current_user.id).all()

	return render_template('chats.html', chats=chats)

@app.route('/buy/<string:domein_name>/<int:price>/<int:s_id>')
def buy(domein_name, price, s_id):
	session['payment_amount'] = price
	session['domein_name'] = domein_name
	session['subdomein_id'] = s_id

	return redirect(url_for('payment', carding=0))


@app.route('/payment/<carding>', methods=['POST', 'GET'])
def payment(carding):
	if carding == '1':
		return render_template('payment.html', carding=True)
	
	if request.method == 'POST':
		account_number = request.form.get('account_number')
		company_account_number = HSBankAccount.query.first()

		data = {
			'get_account_number': account_number,
			'give_account_number': company_account_number.account_number,
			'amount': session['payment_amount']
		}

		response = requests.post(bank_api + 'api/payment/', data=data)
		print(response)
		if response:
			response = response.json()
			if response['message'] == 'success':
				new_domein = DomeinName(
					name = session['domein_name'],
					price = session['payment_amount'],
					subdomein_id = session['subdomein_id'],
					user_id = current_user.id
				)

				db.session.add(new_domein)
				db.session.commit()

				flash(f"Successfully Cash! {response['message']} {response['data']}$")
				return redirect(url_for('home'))
			else:
				flash(f"{response['message']} {response['data']}")
				return redirect(url_for('home'))
		else:
			flash('Server not responding!')
			return redirect(url_for('home'))

	return render_template('payment.html')


@app.route('/messenger/<int:user_id>', methods=['POST', 'GET'])
def messenger(user_id):
	user = User.query.filter_by(id=user_id).first()
	messeges = Messege.query.filter_by(send_user_id=user.id, owner_id=current_user.id).all()
	if request.method == 'POST':
		msg = request.form.get('msg').strip()
		owner_id = current_user.id

		if not msg:
			flash('Please complete the input and then send!')
			return redirect(url_for('messenger', user_id=user_id))

		chat = Chat.query.filter_by(first_member_id=owner_id, second_member_id=user_id).first()

		if not chat:
			new_chat = Chat(
				first_member_id = owner_id,
				second_member_id = user.id
			)

			db.session.add(new_chat)
			db.session.commit()

		new_msg = Messege(
			owner_id = owner_id,
			content = msg,
			send_user_id = user.id,
			chat_id = new_chat.id if not chat else chat.id
		)
		

		db.session.add(new_msg)
		db.session.commit()

		return redirect(url_for('messenger', user_id=1))
	return render_template('messenger.html', user=user, messeges=messeges)


@app.route('/messenger/chat/<int:chat_id>', methods=['POST', "GET"])
def chat(chat_id):
	chat = Chat.query.get(chat_id)
	messeges = Messege.query.filter(Messege.owner_id == chat.first_member_id or Messege.owner_id == chat.second_member_id or Messege.send_user_id == chat.first_member_id or Messege.send_user_id == chat.second_member_id).all()

	if request.method == 'POST':
		msg = request.form.get('msg').strip()
		owner_id = current_user.id

		if not msg:
			flash('Please complete the input and then send!')
			return redirect(url_for('messenger', user_id=chat.second_user_id))

		new_msg = Messege(
			owner_id = owner_id,
			content = msg,
			send_user_id = chat.second_member_id,
			chat_id = chat.id
		)
		

		db.session.add(new_msg)
		db.session.commit()

		return redirect(url_for('chat', chat_id=chat.id))

	return render_template('messenger.html', messeges=messeges, chat=chat)

