import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from app.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
  if request.method == 'POST':
    password = request.form['password']
    email = request.form['email']
    error = None

    if not password:
      error = 'Password is required.'
    elif not email:
      error = 'Email is required.'

    if error is None:
      try:
        # insert the user data into the database
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO customers (email, password) VALUES (%s, %s)', (email, generate_password_hash(password)))
        db.commit()
      except db.IntegrityError:
        error = f"User {email} is already registered."
      else:
        return redirect(url_for("auth.login"))

    flash(error)
    
  return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
  if request.method == 'POST':
    password = request.form['password']
    email = request.form['email']
    error = None

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM customers WHERE email = %s', (email,))
    customer = cursor.fetchone()

    if customer is None:
      error = 'Incorrect email.'
    elif not check_password_hash(customer['password'], password):
      error = 'Incorrect password.'

    if error is None:
      session.clear()
      session['user_id'] = customer['id']
      return redirect(url_for("index"))

    flash(error)

  return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
  user_id = session.get('user_id')

  if user_id is None:
    g.user = None
  else:
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM customers WHERE id = %s', (user_id,))
    g.user = cursor.fetchone()

@bp.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('index'))

def login_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.user is None:
      return redirect(url_for('auth.login'))

    return view(**kwargs)
  return wrapped_view