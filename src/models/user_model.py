from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base_settings_models import BaseModel
from sqlalchemy import SQLAlchemyBaseUserTable


class User(SQLAlchemyBaseUserTable, BaseModel):
    __tablename__ = 'users'
    login = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(1024), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=True)
    surname = Column(String(255), nullable=True)
    born = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    avatar = Column(String(255), nullable=True)
    albom = relationship('alboms', back_populates='user')
    group = relationship('groups', base_populates='group')


class AlbomUser(BaseModel):
    __tablename__ = 'alboms'
    name = Column(String(255), nullable=True, default="my albom")
    user = relationship('user', base_kwargs='albom_user')
    image = relationship('images', back_populates='albom_image')
    user_id = Column(Integer, ForeignKey('users.id'))


class Image(BaseModel):
    __tablename__ = 'images'
    image_url = Column(String(255), nullable=False)
    albom = relationship('albom', back_populates='images')
    albom_id = Column(Integer, ForeignKey('alboms.id'))


class Group(BaseModel):
    __tablename__ = 'group'
    name = Column(String(255), nullable=False)
    user = relationship('user', back_populates='group')
    user_id = Column(Integer,ForeignKey('users.id'))


class Subject(BaseModel):
    __tablename__ ='subjects'
    name = Column(String(255), nullable=False)
    user = relationship('user', back_populates='subject')
    user_id = Column(Integer,ForeignKey('users.id'))


class Category(BaseModel):
    __tablename__ = 'category'
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    course_id = Column(Integer, ForeignKey('course.id'))


class Course(BaseModel):
    __tablename__ ='course'
    name = Column(String(255), nullable=False)
    description = Column(Text)
    users_following = Column(Integer,)
    author_id = Column(Integer,ForeignKey('users.id'))
    category = relationship('category', back_populates='course')
    tasks = relationship('task',back_populates='course')

class Topic(BaseModel):
    __tablename__ = 'topic'
    topic = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    tasks = relationship('task',back_populates='block_quiz')


class Task(BaseModel):
    __tablename__ = 'task'
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    answer_true = Column(String(255),nullable=False)
    topic_id = Column(Integer, ForeignKey('topic.id'))
    course = relationship('course', back_populates='tasks')


class Quiz(BaseModel):
    __tablename__ = 'quiz'
    balls = Column(Integer, nullable=True,default=0)

    user_id = Column(Integer, ForeignKey('users.id'))


class AnswerUser(BaseModel):
    __tablename__ = 'answer_user'
    task_id = Column(Integer,ForeignKey('task.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    quiz_id = Column(Integer,ForeignKey('quiz.id'))
    user_answer = Column(String(255), nullable=True)
    quiz = relationship('quiz', back_populates='answer_user')
    task = relationship('task', back_populates='tasks')

