from flask_app import app, render_template, request, redirect, session, jsonify
from flask_app.models.expense import Expense
from flask_app.models.category import Category
from flask_app.models.user import User
from flask_app.models.fund import Fund

# ! dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {'id':session['user_id']}
    return render_template('dashboard.html', expense = Expense.total_expense(data), savings = User.get_savings(data), all_expenses = Expense.all_expenses(data), monthly_income = Expense.get_monthly_income(data), all_funds = Fund.all_funds(data))

# ! view expenses
@app.route('/expenses')
def expenses():
    if 'user_id' not in session:
        return redirect('/logout')
    categories = Category.get_all_categories()
    print(request.form)
    # print([i.category_title for i in categories])
    return render_template('expenses.html', categories = categories)
# ! view expenses post route
@app.route('/add/expense', methods=['POST'])
def add_expense():
    Expense.create_expense(request.form)
    print(request.form)
    return redirect('/dashboard')

# # ! view all expenses 
@app.route('/expenses/list')
def expenses_list():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {'id':session['user_id']}
    return render_template('view_all_expenses.html', expenses = Expense.all_expenses(data))

# ! generate json file
@app.route('/data')
def data():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {'id':session['user_id']}
    json_expense = Category.get_total_by_category(data)
    print(json_expense)
    return jsonify(json_expense)

@app.route('/reports')
def reports():
    return render_template('reports.html')

#! Fund section
@app.route('/new/fund')
def new_fund():
    if 'user_id' not in session:
        return redirect('/logout')
    categories = Category.get_all_categories()
    return render_template('new_fund.html', categories = categories)
#!add fund post route
@app.route('/add/fund', methods=['POST'])
def add_fund():
    print(request.form)
    Fund.create_fund(request.form)
    return redirect('/dashboard')

# ! edit expense/
@app.route('/edit/expense/<int:id>')
def edit_expense(id):
    # if 'user_id' not in session:
    #     return redirect('/logout')
    data = {'id': id}
    categories = Category.get_all_categories()
    return render_template('edit_expense.html', categories = categories, expense = Expense.get_one_expense(data))
# ! post route for edit expense
@app.route('/update/expense', methods=['POST'])
def update_expense():
    Expense.edit_expense(request.form)
    return redirect("/dashboard")

# ! delete expense:
@app.route('/delete/<int:id>')
def delete(id):
    data = {'id':id}
    Expense.delete_expense(data)
    return redirect('/dashboard')


#  EDIT AND DELETE FUNDS

# ! edit fund
@app.route('/edit/fund/<int:id>')
def edit_fund(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {'id': id}
    categories = Category.get_all_categories()
    return render_template('edit_fund.html', categories = categories, fund = Fund.get_one_fund(data))
# ! post route for edit fund
@app.route('/update/fund', methods=['POST'])
def update_fund():
    Fund.edit_fund(request.form)
    return redirect("/dashboard")

# ! delete fund:
@app.route('/delete/<int:id>')
def delete_fund(id):
    data = {'id':id}
    Fund.delete_fund(data)
    return redirect('/dashboard')




