from app import db,app
from sqlalchemy import Column, types,FLOAT
from sqlalchemy import create_engine,engine
from flask_login import current_user,login_manager
from flask_login import UserMixin
engine = create_engine('mysql+mysqlconnector://ldnapm80t9dh5dce:ftm6ffn1bjyavcdu@u3r5w4ayhxzdrw87.cbetxkdyhwsb.us-east-1.rds.amazonaws.com/qw4h0rr8ia06zybf', convert_unicode=True)



class users(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer,primary_key = True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100),unique = True)
    password=db.Column(db.String(200))
    role_id=db.Column(db.Integer,db.ForeignKey('role.id'))
    def __init__(self,*args,**kwargs):
        super(users,self).__init__(*args,**kwargs)

    def __repr__(self):
        return self.full_name
 
class state(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100))
    state_univer = db.relationship('university',backref = 'state')
    def __init__(self, *args, **kwargs):  
        super(state,self).__init__(*args,**kwargs)

    def __repr__(self):
        return self.name

class role(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer,primary_key = True)
    role = db.Column(db.String(100))
    user_role = db.relationship('users', backref='role')

    def __init__(self, *args, **kwargs):  
        super(role,self).__init__(*args,**kwargs)

    def __repr__(self):
        return self.role

class university(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100))
    department = db.relationship('department', backref='university')
    state_id = db.Column(db.Integer,db.ForeignKey('state.id'))
    logo = db.Column(db.String(200))
    university_picture = db.Column(db.String(200))
    int_university = db.relationship('international_universities',backref = 'univer_id')
    desc = db.Column(db.String(1000))
    def __init__(self, *args, **kwargs):  
        super(university,self).__init__(*args,**kwargs)

    def __repr__(self):
        return self.name

class department(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100))
    university_id=db.Column(db.Integer,db.ForeignKey('university.id'))
    price = db.Column(db.Integer)
    duration = db.Column(db.Integer) 
    degree = db.Column(db.Integer,db.ForeignKey('degree.id'))
    def __init__(self, *args, **kwargs):  
        super(department,self).__init__(*args,**kwargs)

    def __repr__(self):
        return self.name

class degree(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    depart_degree = db.relationship('department',backref = 'dep_degree')
    
    def __init__(self, *args, **kwargs):  
        super(degree,self).__init__(*args,**kwargs)

    def __repr__(self):
        return self.name

class international_universities(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(200))
    university_id = db.Column(db.Integer,db.ForeignKey('university.id'))
    link = db.Column(db.String(400))
    country = db.Column(db.Integer,db.ForeignKey('country.id'))
    def __init__(self, *args, **kwargs):  
        super(international_universities,self).__init__(*args,**kwargs)

    def __repr__(self):
        return self.name

class country(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    flag = db.Column(db.String(100))
    int_university = db.relationship('international_universities', backref = 'country_name')
    def __init__(self, *args, **kwargs):  
        super(country,self).__init__(*args,**kwargs)

    def __repr__(self):
        return self.name




