# from flask_sqlalchemy import SQLAlchemy
# # from sqlalchemy import DeclarativeBase
# from flask import Flask, request, jsonify

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bills.db'

# db = SQLAlchemy(app)

# # Define the User and Bill models
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username
    
# class Bill(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     description = db.Column(db.String(100), nullable=False)
#     total = db.Column(db.Float, nullable=False)
#     paid_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     participants = db.relationship('User', backref=db.backref('bills', lazy=True))

#     def __repr__(self):
#         return '<Bill %r>' % self.total
    
# db.create_all()



# # Routes
# @app.route('/register', methods=['POST'])
# class register():
#     data = request.get_json()