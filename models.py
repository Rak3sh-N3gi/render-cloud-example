import os
import sys
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Person
Have title and release year
'''
class Person(db.Model):  
  __tablename__ = 'People'

  id = Column(db.Integer, primary_key=True)
  name = Column(String)
  catchphrase = Column(String)

  def __init__(self, name, catchphrase=""):
    self.name = name
    self.catchphrase = catchphrase

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'catchphrase': self.catchphrase}
  
class Movies(db.Model):
  __tablename__ = 'Movies'
  id = Column(db.Integer, primary_key=True)
  title = Column(String)
  release_date = Column(String)

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date}
  
  def __repr__(self):
    return json.dumps(self.format())
  
  #display movie details by id
  def display(id):
    movies = Movies.query.filter(Movies.id == id).one_or_none()
    return format(movies)
  
  # display all movies
  def display_all():
    movies = Movies.query.all()
    return format(movies)
    
  #insert movie details
  def insert(self):
    rc = 0
    try:
      db.session.add(self)
      db.session.commit()
      rc = self.id
    except:
      db.session.rollback()
      print(sys.exc_info())
      db.session.flush()
    finally:
      db.session.close()
    return rc
    
# update Movies details, All the details are mandatory
  def update(id,title,release_date):
    rc = 0
    try:
      rc = db.session.query(Movies).filter(Movies.id == id).update({Movies.title: title, Movies.release_date: release_date})
      db.session.commit()
    except:
      db.session.rollback()
      print(sys.exc_info())
      db.session.flush()
    finally:
      db.session.close()
    return rc
  
# delete movie details
  def delete(id):
    rc = 0
    try:
      rc = db.session.query(Movies).filter(Movies.id == id).delete()
      db.session.commit()
    except:
      db.session.rollback()
      print(sys.exc_info())
      db.session.flush()
    finally:
      db.session.close()
    return rc
  
class Actors(db.Model):
  __tablename__ = 'Actors'
  id = Column(db.Integer, primary_key=True)
  name = Column(String)
  age = Column(db.Integer)
  gender = Column(String)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender}
  
  def __repr__(self):
    return json.dumps(self.format())
  
  # display actor details by id
  def display(id):
    actors = Actors.query.filter(Actors.id == id).one_or_none()
    if actors is None:
      return None
    else:
      return format(actors)
  
  # display all actors
  def display_all():
    actors = Actors.query.all()
    return format(actors)

  # insert Actor details
  def insert(self):
    rc = 0
    try:
      db.session.add(self)
      db.session.commit()
      rc = self.id
    except:
      db.session.rollback()
      print(sys.exc_info())
      db.session.flush()
    finally:
      db.session.close()
    return rc

  # update Actor details, All the details are mandatory
  def update(id,name,age,gender):
    rc = 0
    try:
      rc = db.session.query(Actors).filter(Actors.id == id).update({Actors.name: name, Actors.age: age,Actors.gender:gender})
      db.session.commit()
    except:
      db.session.rollback()
      print(sys.exc_info())
      db.session.flush()
    finally:
      db.session.close()
    return rc
    
  # delete Actor details
  def delete(id):
    rc = 0
    try:
      rc = db.session.query(Actors).filter(Actors.id == id).delete()
      db.session.commit()
    except:
      db.session.rollback()
      print(sys.exc_info())
      db.session.flush()
    finally:
      db.session.close()
    return rc
