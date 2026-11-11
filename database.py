from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    image = Column(String, nullable=True)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    caption = Column(Text, nullable=True)
    image = Column(String, nullable=True)  # Allow image to be nullable
    likes = Column(Integer, default=0)
    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post', cascade='all, delete-orphan')

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    user = relationship('User')
    post = relationship('Post', back_populates='comments')

class Workout(Base):
    __tablename__ = 'workouts'
    id = Column(Integer, primary_key=True)
    exercise = Column(String, nullable=False)
    muscle_group = Column(String, nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    date = Column(Date, nullable=False)


User.posts = relationship('Post', order_by=Post.id, back_populates='user')

# Create an engine that stores data in the local directory's
# sqlite database file
engine = create_engine('sqlite:///sociallyfit.db')

# Create all tables in the engine
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session
session = Session()

def add_workout(workout):
    with Session() as s:
        s.add(Workout(**workout))
        s.commit()

def get_workouts():
    with Session() as s:
        rows = s.query(Workout).order_by(Workout.date).all()
        return [
            {'exercise': w.exercise, 'muscle_group': w.muscle_group,
             'sets': w.sets, 'reps': w.reps, 'weight': w.weight, 'date': w.date}
            for w in rows
        ]