from website import *
from .models import *
from .auth import login, logout, register
from flask_login import LoginManager, login_required, current_user, login_user, logout_user

# Login manager 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_func'


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
				check = DomeinName.query.filter_by(name = domein_name, subdomein_id = s.id).first()
				if not check:
					result[domein_name+s.name] = 'available'
				if check:
					result[domein_name+s.name] = 'not available'
			return render_template('domein_selling.html', subdomeins=subdomeins, result=result, list=True)

		check = DomeinName.query.filter_by(name = domein_name, subdomein_id = subdomein.id).first()

		if check:
			result = {'domein_name': f'{domein_name}{subdomein}',
						'type': 'not available'
					}
		elif not check:
			result = {'domein_name': f'{domein_name}{subdomein}', 
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


@app.route('/payment/<carding>')
def payment(carding):
	if carding == '1':
		return render_template('payment.html', carding=True)
	
	return render_template('payment.html')