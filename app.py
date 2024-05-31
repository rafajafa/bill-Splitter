from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newdatabase.db'
app.config['SECRET_KEY'] = 'testsecretkey'
db = SQLAlchemy(app)
app.app_context().push()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    # return User.query.get(int(user_id))
    return db.session.get(User, int(user_id))

# Define the association table
group_user = db.Table('group_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    # group = db.relationship('Group', backref=db.backref('user', lazy=True))
    group = db.relationship('Group', secondary=group_user, backref = db.backref('users', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, new_password):
        self.password = new_password
    

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    members = db.relationship('User', secondary='group_user', backref=db.backref('groups', lazy=True))
    # bills = db.relationship('Bill', backref=db.backref('group', lazy=True))

    def __repr__(self):
        return '<Group %r>' % self.name
    
    def add_member(self, user):
        self.members.append(user)
    
class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Float, nullable=False)
    paid_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    
    # participants = db.relationship('User', secondary='bill_user', backref=db.backref('bills', lazy=True))
    
    def __repr__(self):
        return '<Bill %r>' % self.description

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Username"})
    email = StringField(validators=[InputRequired(), Email(), Length(min=2, max=30)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=2, max=30)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Error: Username already exists')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Error: Email already exists')

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=2, max=30)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField('Login')

class GroupForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=2, max=100)], render_kw={"placeholder": "Name"})
    submit = SubmitField('Create Group')
    
class JoinGroupForm(FlaskForm):
    group_name = StringField(validators=[InputRequired(), Length(min=2, max=100)], render_kw={"placeholder": "Group Name"})
    submit = SubmitField('Join Group')

class BillForm(FlaskForm):
    description = StringField(validators=[InputRequired(), Length(min=2, max=100)], render_kw={"placeholder": "Description"})
    total = StringField(validators=[InputRequired()], render_kw={"placeholder": "Total"})
    paid_by_username = StringField(validators=[InputRequired()], render_kw={"placeholder": "Paid by"})
    participants = StringField(validators=[InputRequired()], render_kw={"placeholder": "Participants"})
    
    group = StringField(validators=[InputRequired()], render_kw={"placeholder": "Group"})
    
    submit = SubmitField('Add Bill')

    def validate_paid_by_username(self, paid_by_username):
        user = User.query.filter_by(username=paid_by_username.data).first()
        if not user:
            raise ValidationError('User does not exist')
    
    def validate_participants(self, participants):
        for user_id in participants.data.split(','):
            user = User.query.get(user_id)
            if not user:
                raise ValidationError(f'User with id {user_id} does not exist')

    def validate_group(self, group):
        group = Group.query.filter_by(name=group.data).first()
        if not group:
            raise ValidationError('Group does not exist')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        
        print("new user added to db")
        
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            print("User logged in")
            login_user(user)
            return redirect(url_for('dashboard'))
    
    return render_template('login.html', form = form)

@app.route('/dashboard')
@login_required
def dashboard():
    user_groups = current_user.groups
    return render_template('dashboard.html', groups=user_groups)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    form = GroupForm()
    if form.validate_on_submit():
        # create a new group
        new_group = Group(name=form.name.data)
        db.session.add(new_group)
        db.session.commit()
        
        # add the current user to the group
        new_group.add_member(current_user)
        db.session.commit()
        # add the group to the current user
        current_user.groups.append(new_group)
        return redirect(url_for('dashboard'))
    
    return render_template('create_group.html', form=form)

@app.route('/add_bill', methods=['GET', 'POST'])
@login_required
def add_bill():
    form = BillForm()
    if form.validate_on_submit():
        new_bill = Bill(description=form.description.data, 
                        total = form.total.data, 
                        paid = form.paid_by_username.data,
                        participants = form.participants.data,
                        group = form.group.data)
        db.session.add(new_bill)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_bill.html', form=form)

@app.route('/join_group')
@login_required
def join_group():
    form = JoinGroupForm()
    return render_template('join_group.html', form=form)

@app.route('/group/<int:group_id>')
@login_required
def group_detail(group_id):
    group = Group.query.get(group_id)
    return render_template('group_detail.html', group=group)

with app.app_context():
    db.create_all()
    new_user = User(username='tester', email="test@example.com")
    new_user.set_password('1234')
    db.session.add(new_user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
    users = User.query.all()
    print(users)
    for user in users:
        print(user.username, user.email, user.password)
    

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
