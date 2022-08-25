from crypt import methods
from flask_app import app, render_template, request, redirect, session, bcrypt, flash
from flask_app.models.user import User
from flask_app.models.expense import Expense


# ! ROOT ROUTE
@app.route('/')
def index():
    return render_template('index.html')

# ! REGISTER A USER
@app.route('/register', methods = ['post'])
def register():
    ## validate them
    print(request.form)
    # check if there is a user already with this email in our db
    data = {'email': request.form['email']}
    user_in_db =  User.get_one_with_email(data)
    if user_in_db:
        flash('Email already registered.', 'email')
        return redirect('/')
    # validate all fields
    if not User.validate_user(request.form):
        return redirect('/logout')
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    print(hashed_pw)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashed_pw
    }
    print(data)
    ## add user to database
    user_id = User.save_user(data)
    ## log in the user by adding them to session
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    return redirect('/add/info')

# ! LOGIN
@app.route('/login', methods = ['post'])
def login():
    ## check the database for the email they enter
    data = {'email': request.form['log_email']}
    user_in_db = User.get_one_with_email(data)
    if not user_in_db:
        flash("invalid credentials")
        return redirect('/')
    ## check the password the supply matches the hash in the database
    if not bcrypt.check_password_hash(user_in_db.password, request.form['log_password']):
        flash("invalid credentials")
        return redirect('/logout')
    ## log in the use by adding to session
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    return redirect('/dashboard')


# ! LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    pass

# ! EDIT ACCOUNT
@app.route('/edit/user/')
def update_user():
    data = {'id':session['user_id']}
    return render_template('edit_user.html', user = User.get_one(data))
#! EDIT ACCOUNT: POST ROUTE
@app.route('/update/user/', methods=['POST'])
def edit_user():
    if not User.validate_user(request.form):
        return redirect('/edit/user')
    User.edit_user(request.form)
    return redirect("/dashboard")

# ! update savings
@app.route('/savings')
def savings():
    if 'user_id' not in session:
        return redirect('/logout')
    # print([i.category_title for i in categories])
    data = {'id':session['user_id']}
    return render_template('savings.html', savings = User.get_savings(data))
# ! add savings post route
@app.route('/add/savings', methods=['POST'])
def add_savings():
    User.update_savings(request.form)
    return redirect('/dashboard')

# ! add user info (savings and income)
@app.route('/add/info')
def info():
    if 'user_id' not in session:
        return redirect('logout')
    if not User.validate_info(request.form):
        return redirect('/user/info')
    return render_template('post_reg_form.html')

# ! user info post route
@app.route('/update/info', methods=['POST'])
def add_info():
    print(request.form)
    User.get_income_savings(request.form)
    return redirect('/dashboard')
