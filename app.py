from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)  # Plain text password storage
    status = db.Column(db.Boolean, nullable=False)  # 1 for employee, 0 for employer
    summary = db.Column(db.String(100), default='')
    description = db.Column(db.String(500), default='')


# Initialize the database with tables
with app.app_context():
    db.create_all()

# Load user function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@login_required
def home():
    role = "Employee" if current_user.status == 1 else "Employer"
    return render_template('home.html', name=current_user.username, role=role)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:  # Check plain text password
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        checkbox = request.form.get('checkbox')
        status = 1 if checkbox else 0  # 1 for employee, 0 for employer

        new_user = User(username=username, password=password, status=status, summary='', description='')
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfully')
            return redirect(url_for('login'))
        except:
            flash('Username already exists')
    return render_template('signup.html')


@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        # Update the current user's profile fields
        current_user.summary = request.form.get('summary')
        current_user.description = request.form.get('description')
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('update_profile'))

    # Pass the current user's data to the template
    return render_template(
        'update_profile.html',
        username=current_user.username,
        summary=current_user.summary,
        description=current_user.description
    )
@app.route('/settings')
@login_required
def settings():
    # Render a settings page or perform settings-related actions
    return render_template('settings.html')
@app.route('/chats')
@login_required
def chats():
    return render_template('chats.html')
@app.route('/notifications')
@login_required
def notifications():
    return render_template('notifications.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
