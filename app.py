from flask import Flask, render_template, request, redirect, session, url_for, flash
from config import Config
from models import db, bcrypt, FirstApp, User
from forms import PersonForm, LoginForm
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)

db.init_app(app)
bcrypt.init_app(app)

@app.before_request
def make_session_permanent():
    session.permanent = True

# Create DB and default user if needed
with app.app_context():
    os.makedirs(os.path.join(os.path.dirname(__file__), 'instance'), exist_ok=True)
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='shah')
        admin.set_password('Srk12345')   # NOTE: change in production
        db.session.add(admin)
        db.session.commit()

# ---- Routes ----
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user'] = username
            flash("Login successful", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password", "danger")
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out", "info")
    return redirect(url_for('login'))

@app.route('/', methods=['GET','POST'])
def index():
    if 'user' not in session:
        return redirect(url_for('login'))

    form = PersonForm()
    if form.validate_on_submit():
        # ORM usage (parameterized at driver level)
        p = FirstApp(fname=form.fname.data.strip(),
                     lname=form.lname.data.strip(),
                     email=form.email.data.strip())
        db.session.add(p)
        db.session.commit()
        flash("Record added", "success")
        return redirect(url_for('index'))

    people = FirstApp.query.all()
    return render_template('index.html', allpeople=people, form=form)

@app.route('/delete/<int:sno>', methods=['POST'])
@csrf.exempt  # or better: send POST with CSRF token from client
def delete(sno):
    if 'user' not in session:
        return redirect(url_for('login'))
    person = FirstApp.query.filter_by(sno=sno).first_or_404()
    db.session.delete(person)
    db.session.commit()
    flash("Deleted successfully", "info")
    return redirect(url_for('index'))

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if 'user' not in session:
        return redirect(url_for('login'))
    person = FirstApp.query.filter_by(sno=sno).first_or_404()
    form = PersonForm(obj=person)
    if form.validate_on_submit():
        person.fname = form.fname.data.strip()
        person.lname = form.lname.data.strip()
        person.email = form.email.data.strip()
        db.session.commit()
        flash("Updated successfully", "success")
        return redirect(url_for('index'))
    return render_template('update.html', allpeople=person, form=form)

# ---- Custom error handlers (secure error handling) ----
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    # do not reveal exception details
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)
