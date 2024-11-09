from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_BINDS'] = {
    'db2': 'sqlite:///db2.sqlite3',  # db2 is for employees and db3 for employers
    'db3': 'sqlite:///db3.sqlite3'
}

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
    

class Model2(db.Model):
    __tablename__ = '2Model'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    status = db.Column(db.Boolean, nullable=False)  # 1 for employee, 0 for employer
    summary = db.Column(db.String(100), default='')
    description = db.Column(db.String(500), default='')


class Model3(db.Model):
    __bind_key__ = 'db3'
    __tablename__ = '3Model'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    status = db.Column(db.Boolean, nullable=False)  # 1 for employee, 0 for employer
    summary = db.Column(db.String(100), default='')
    description = db.Column(db.String(500), default='')


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@login_required
def home():
    role = "Employee" if current_user.status == 1 else "Employer"
    return render_template('home.html', name=current_user.username, role=role)

@app.route('/job', methods=['GET', 'POST'])
def job():
    if request.method == 'POST':
        job_title = request.form['jobname']
        user_id = request.form['user_id']

        # Find or create the job
        job = Job.query.filter_by(title=job_title).first()
        if not job:
            job = Job(title=job_title)
            db.session.add(job)
        
        # Associate the user with the job
        user = User.query.get(user_id)
        if user and user not in job.users:
            job.users.append(user)
        
        try:
            db.session.commit()
            flash('Job and user association created successfully')
            return redirect(url_for('job'))
        except:
            db.session.rollback()
            flash('Job already exists or association failed')
    
    jobs = Job.query.all()  # Fetch all jobs with associated users
    users = User.query.all()  # For populating the dropdown
    return render_template('job.html', jobs=jobs, users=users)

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

            if status == 1:
                employee_entry = Model2(username=username, password=password, status=status, summary='', description='')
                db.session.add(employee_entry)
                db.session.commit()
            else:
                employer_entry = Model3(username=username, password=password, status=status, summary='', description='')
                db.session.add(employer_entry)
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

    # Retrieve the jobs associated with the current user
    user_jobs = current_user.jobs

    return render_template(
        'update_profile.html',
        username=current_user.username,
        summary=current_user.summary,
        description=current_user.description,
        jobs=user_jobs  # Pass jobs to the template
    )


@app.route('/settings')
@login_required
def settings():
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
