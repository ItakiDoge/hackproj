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

user_jobs = db.Table('user_jobs',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('job_id', db.Integer, db.ForeignKey('jobs.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    status = db.Column(db.Boolean, nullable=False)  # 1 for employee, 0 for employer
    summary = db.Column(db.String(100), default='')
    description = db.Column(db.String(500), default='')

    jobs = db.relationship('Job', secondary=user_jobs, back_populates="users")

class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=True, nullable=False)

    users = db.relationship('User', secondary=user_jobs, back_populates="jobs")

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def home():
    role = "Employee" if current_user.status == 1 else "Employer"
    if role == "Employee": 
        jobs = Job.query.all()
        return render_template('home.html', name=current_user.username, role=role, jobs=jobs)
    else: 
        jobs = Job.query.filter(Job.users.any()).all()
        return render_template('home.html', name=current_user.username, role=role, jobs=jobs)

@app.route('/notify/<int:job_id>/<int:user_id>', methods=['POST'])
@login_required
def notify(job_id, user_id):
    if current_user.status == 0:  # Only employers can notify
        explanation = request.form.get('explanation')
        decision = request.form.get('decision')
        job = Job.query.get(job_id)
        user = User.query.get(user_id)

        if decision == 'accepted':
            message = f"You have been accepted for Job ID {job_id}. Further hiring process will commence. Explanation: {explanation}"
        else:  # Handle rejection
            message = f"Your application for Job ID {job_id} was rejected. Explanation: {explanation}"
            if user in job.users:
                job.users.remove(user)  # Remove the user from the job if rejected

        # Create and save the notification
        notification = Notification(user_id=user_id, message=message)
        db.session.add(notification)
        db.session.commit()
        flash('Notification sent to the user.')
    return redirect(url_for('home'))

@app.route('/notifications')
@login_required
def notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).all()
    messages = [n.message for n in notifications]
    return render_template('notifications.html', messages=messages)

@app.route('/select_job/<int:job_id>', methods=['POST'])
@login_required
def select_job(job_id):
    job = Job.query.get(job_id)
    if job and current_user not in job.users:
        job.users.append(current_user)
        db.session.commit()
        flash(f'Successfully applied for {job.title}')
    else:
        flash('You have already applied for this job or it does not exist')
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
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
            db.session.rollback()
            flash('Username already exists')
    return render_template('signup.html')

@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        current_user.summary = request.form.get('summary')
        current_user.description = request.form.get('description')
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('update_profile'))

    user_jobs = current_user.jobs

    return render_template(
        'update_profile.html',
        username=current_user.username,
        summary=current_user.summary,
        description=current_user.description,
        jobs=user_jobs
    )

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@app.route('/chats')
@login_required
def chats():
    return render_template('chats.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
