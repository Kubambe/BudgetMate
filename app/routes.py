from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Expense, User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        title = request.form['title']
        amount = float(request.form['amount'])
        category = request.form['category']
        receipt = request.files.get('receipt')
        receipt_filename = None
        if receipt:
            receipt_filename = secure_filename(receipt.filename)
            receipt.save(os.path.join(app.config['UPLOAD_FOLDER'], receipt_filename))
        
        new_expense = Expense(title=title, amount=amount, category=category, user_id=current_user.id, receipt_image=receipt_filename)
        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
    
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', expenses=expenses)

@app.route('/reports', methods=['GET'])
@login_required
def reports():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    return render_template('reports.html', expenses=expenses)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    if request.method == 'POST':
        new_category = request.form['category']
        # Logic to store the category
        flash('Category added successfully!', 'success')
    categories = []  # Retrieve categories from the database
    return render_template('categories.html', categories=categories)

@app.route('/monthly_overview')
@login_required
def monthly_overview():
    monthly_data = {}
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    for expense in expenses:
        month = expense.date.strftime("%B")
        if month not in monthly_data:
            monthly_data[month] = 0
        monthly_data[month] += expense.amount
    return render_template('monthly_overview.html', monthly_data=monthly_data)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
