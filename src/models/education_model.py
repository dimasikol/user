import random
import datetime

import uvicorn
from fastapi import FastAPI, Depends, Body,Form,Query,Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.sql import func
from typing import Annotated
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey, Text,text
from sqlalchemy.orm import DeclarativeBase,Session, Mapped, mapped_column
from sqlalchemy import MetaData

metadata_obj = MetaData()

engine = create_engine("sqlite:///data.sqlite3", echo=True)

str36_unique = Annotated[str,mapped_column(String(36),unique=True,nullable=False)]
str24 = Annotated[str,mapped_column(String(24),nullable=True)]
image = Annotated[str,mapped_column(String(50),nullable=True)]


class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)

BaseModel.metadata.create_all(bind=engine)


class TimeModel(DeclarativeBase):
    created_at: Mapped[datetime.datetime|None] = mapped_column(default=func.now())
    updated_at: Mapped[datetime.datetime|None] = mapped_column(default=func.now(), onupdate=func.now())


class User(BaseModel,TimeModel):
    __tablename__ = 'users'
    login: Mapped[str36_unique]
    hashed_password: Mapped[str | None] = mapped_column(String(64), nullable=False)
    email: Mapped[str36_unique]
    name: Mapped[str24]
    surname: Mapped[str24]
    born: Mapped[datetime.date | None]
    is_active: Mapped[bool | None] = mapped_column(Boolean, default=True)
    avatar: Mapped[image]

    albom = relationship('AlbomUser', back_populates='user')
    group = relationship('Group', back_populates='user')
    course = relationship('Course', back_populates='user')
    quiz = relationship('QuizBlock',back_populates='user')
    subject = relationship('Subject', back_populates='user')
    quiz_block = relationship('QuizBlock',back_populates='user')
class Image(BaseModel,TimeModel):
    __tablename__ = 'images'
    image_url: Mapped[str]

    albom_id: Mapped[int] = mapped_column(ForeignKey('alboms.id',ondelete="CASCADE"))

    albom = relationship('AlbomUser', back_populates='image')


class AlbomUser(BaseModel,TimeModel):
    __tablename__ = 'alboms'
    name: Mapped[str24]
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id',ondelete="CASCADE"))

    user = relationship('User', back_populates='albom')
    image = relationship('Image', back_populates='albom', )


class Group(BaseModel,TimeModel):
    __tablename__ = 'group'
    name: Mapped[str36_unique]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id',ondelete="CASCADE"))

    user = relationship('User', back_populates='group')


class Subject(BaseModel,TimeModel):
    __tablename__ ='subjects'
    name: Mapped[str] = mapped_column(String(255),nullable=False)

    user_id = Column(Integer,ForeignKey('users.id'))

    user = relationship('User', back_populates='subject')



class Category(BaseModel):
    __tablename__ = 'category'
    name: Mapped[str36_unique]
    description: Mapped[str] = mapped_column(Text,nullable=False)
    image: Mapped[image]

    course = relationship('Course', back_populates='category')


class Course(BaseModel,TimeModel):
    __tablename__ ='course'
    name: Mapped[str36_unique]
    description: Mapped[str] = mapped_column(Text,nullable=True)
    users_following: Mapped[int] = mapped_column(default=0,nullable=True)

    author_id: Mapped[int] = mapped_column(ForeignKey('users.id',ondelete="CASCADE"))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id',ondelete="CASCADE"))

    category = relationship('Category', back_populates='course')
    topic = relationship('Topic',back_populates='course')
    user = relationship('User',back_populates='course')

class Topic(BaseModel,TimeModel):
    __tablename__ = 'topic'
    name: Mapped[str36_unique]
    description: Mapped[str] = mapped_column(Text,nullable=True)

    course_id: Mapped[int] = mapped_column(ForeignKey('course.id',ondelete="CASCADE"))

    tasks = relationship('Task',back_populates='topic')
    course = relationship('Course',back_populates='topic')


class Task(BaseModel,TimeModel):
    __tablename__ = 'task'

    name: Mapped[str] = mapped_column(String(255),nullable=False)
    description: Mapped[str] = mapped_column(Text,nullable=False)

    topic_id: Mapped[int] = mapped_column(ForeignKey('topic.id',ondelete="CASCADE"))

    quiz = relationship('Quiz',back_populates='tasks')
    topic = relationship('Topic', back_populates='tasks')
    quiz_block = relationship('QuizBlock', back_populates='tasks')
class Quiz(BaseModel):
    __tablename__ = 'quiz'
    name: Mapped[str] = mapped_column(String(255),nullable=False)
    description: Mapped[str] = mapped_column(Text,nullable=False)
    answer_true: Mapped[str] = mapped_column(String(255),nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey('category.id',ondelete="CASCADE"))
    task_id: Mapped[int] = mapped_column(ForeignKey('task.id',ondelete="CASCADE"))
    type_quiz_id: Mapped[int] = mapped_column(ForeignKey('type_quiz.id',ondelete="CASCADE"))

    answer_user = relationship('AnswerUser',back_populates='quiz')
    tasks = relationship('Task',back_populates='quiz')

class TypeQuiz(BaseModel):
    __tablename__ = 'type_quiz'
    name: Mapped[str36_unique]
    description: Mapped[str] = mapped_column(Text, nullable=False)


class QuizBlock(BaseModel):
    __tablename__ = 'quiz_block'
    created_at: Mapped[datetime.datetime|None] = mapped_column(default=func.now())

    count_quiz: Mapped[int] = mapped_column(default=0,nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    task_id: Mapped[int] = mapped_column(ForeignKey('task.id', ondelete="CASCADE"))

    user = relationship('User', back_populates='quiz_block')
    tasks = relationship('Task',back_populates='quiz_block')
    answer_user = relationship('AnswerUser',back_populates='quiz_block')

class AnswerUser(BaseModel,TimeModel):
    __tablename__ = 'answer_user'

    answer: Mapped[str | None]

    quiz_id: Mapped[int] = mapped_column(ForeignKey('quiz.id', ondelete="CASCADE"))
    quiz_block_id: Mapped[int] = mapped_column(ForeignKey('quiz_block.id', ondelete="CASCADE"))

    quiz = relationship('Quiz', back_populates='answer_user')
    quiz_block = relationship('QuizBlock', back_populates='answer_user')


def add_user(con,num):
    con.execute(text(f"INSERT INTO users (login, hashed_password, email, name, surname, born, is_active, avatar)"
                     f" VALUES (:login,:hashed_password,:email,:name,:surname,:born,:is_active,:avatar);",),
                {
                    'login': f'admin{num}',
                    'hashed_password': 'hashed_password',
                    'email': f'admin{num}@admin.com',
                    'name': 'admin',
                    'surname': 'admin',
                    'born': datetime.datetime.now(),
                    'is_active': True,
                    'avatar': 'https://cdn.discordapp.com/attachments/'})
    con.commit()

def add_category(con,category,num):
    num = random.randint(0,1000)

    con.execute(text(f"INSERT INTO category (name, description, image) VALUES (:name,:description,:image);"),
                {'name': f'{category}{num}', 'description': 'Python programming language', 'image': 'https://upload.wikimedia.org/wikipedia/commons/'})
    con.commit()

def add_course(con,course,num):
    con.execute(text(f"INSERT INTO course (name,description,users_following,author_id,category_id) VALUES (:name,:description,:users_following,:author_id,:category_id);"),
                {'name':f'oge by infomatic{num}','description':'oge by informatic','users_following':10,'author_id':1,'category_id':1})
    con.commit()

def add_topic(con,topic,num):
    con.execute(text(f"INSERT INTO topic (name, description, course_id) "
                     f"VALUES (:name,:description,:course_id);"),
                {'name':f'topic{num}','description':'description of topic','course_id':1})
    con.commit()

def add_task(con,task,num):
    #name: Mapped[str] = mapped_column(String(255),nullable=False)
    #description: Mapped[str] = mapped_column(Text,nullable=False)
    #topic_id: Mapped[int] = mapped_column(ForeignKey('topic.id',ondelete="CASCADE"))
    con.execute(text(f"INSERT INTO task (name, description, topic_id) "
                     f"VALUES (:name,:description,:topic_id);"),
                {'name':f'task{num}','description':'description of topic','topic_id':1})
    con.commit()

def add_quiz_block(con,task,num):
    # created_at: Mapped[datetime.datetime|None] = mapped_column(default=func.now())
    # count_quiz: Mapped[int] = mapped_column(default=0,nullable=True)
    # user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    # task_id: Mapped[int] = mapped_column(ForeignKey('task.id', ondelete="CASCADE"))
    con.execute(text(f"INSERT INTO quiz_block (count_quiz, user_id, task_id) "
                     f"VALUES (:count_quiz,:user_id,:task_id);"),
                {'count_quiz':f'quiz block{num}','user_id':1,'task_id':1})
    con.commit()

def add_type_quiz(con,type_quiz,num):
    #name:
    #descriptin
    con.execute(text(f"INSERT INTO type_quiz (name, description) VALUES (:name,:description)"),
                {"name":f"tyoe_quiz{num}","description":"description of type_quiz1"})
    con.commit()

def add_quiz(con,quiz,block_quiz,num):
    #name: Mapped[str] = mapped_column(String(255),nullable=False)
    # description: Mapped[str] = mapped_column(Text,nullable=False)
    # answer_true: Mapped[str] = mapped_column(String(255),nullable=False)
    #
    # category_id: Mapped[int] = mapped_column(ForeignKey('category.id',ondelete="CASCADE"))
    # task_id: Mapped[int] = mapped_column(ForeignKey('task.id',ondelete="CASCADE"))
    # type_quiz_id: Mapped[int] = mapped_column(ForeignKey('type_quiz.id',ondelete="CASCADE"))

    con.execute(text(f"INSERT INTO quiz (name, description, answer_true, category_id, task_id,type_quiz_id) "
                     f"VALUES (:name, :description, :answer_true, :category_id, :task_id,:type_quiz_id);"),
                {'name':f'quiz{num}','description':'description of topic','answer_true':'answer_true','category_id':1,'task_id':1,'type_quiz_id':1})
    con.commit()



def add_answer_user(con,num):
    # answer: Mapped[str | None]
    # quiz_id: Mapped[int] = mapped_column(ForeignKey('quiz.id', ondelete="CASCADE"))
    # quiz_block_id: Mapped[int] = mapped_column(ForeignKey('quiz_block.id', ondelete="CASCADE"))

    con.execute(text(f"INSERT INTO answer_user (answer, quiz_id,quiz_block_id) VALUES "
        "(:answer,:quiz_id,:quiz_block_id)"),
         [
             {'answer':f'answer{num}',"quiz_id":1,"quiz_block_id":1},
             {'answer':f'answer{num}',"quiz_id":2,"quiz_block_id":1},
             {'answer':f'answer{num}',"quiz_id":1,"quiz_block_id":2},
             {'answer':f'answer{num}',"quiz_id":2,"quiz_block_id":3},
         ])
    con.commit()


def f():
    pass

def create_db_and_tables():
    with Session(engine) as conn:
        BaseModel.metadata.create_all(bind=engine)
        conn.commit()
        num = random.randint(0,1000)
        add_user(conn, num)
        add_category(conn, f'himick{num}', num)
        add_course(conn, f'oge himick{num}', num)
        add_topic(conn, f'topic{num}', num)
        add_task(conn, f'task{num}', num)
        add_type_quiz(conn, f'type_quiz{num}', num)
        add_quiz(conn, f'quiz{num}', num,num)
        add_quiz_block(conn, f'task{num}',num)
        add_quiz_block(conn, f'task{num}', num)
        add_quiz_block(conn, f'task{num}', num)
        add_quiz_block(conn, f'task{num}', num)
        add_answer_user(conn,  num)
        add_answer_user(conn,  num)


app = FastAPI()

SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def index():
    return HTMLResponse("""
    <a href="/category">1.category</a>
    <a href="/course">2.course</a>
    <a href="/topic">3.topic</a>
    <a href="/task">4.task</a>
    <a href="/quiz">5.quiz</a>
    <a href="/quiz_block">6.quiz block</a>
    <a href="/type_quiz">7.type_quiz</a>
    <a href="/answer_user">8.answer user</a>
    <a href="/user">9.user</a>
    <a href=""></a>
    """)


@app.get('/category/{contry}')
def get_category(contry,request:Request,db: Session = Depends(get_db)):
    print(contry,'город')
    print(request.query_params,"параметры гет запроса")
    return {"data":db.query(Category).all()}


@app.patch('/category')
def get_category(db: Session = Depends(get_db)):
    return {"data":db.query(Category).all()}


@app.get('/category')
def get_category(db: Session = Depends(get_db)):
    return {"data":db.query(Category).order_by(Category.id.desc()).all()}


@app.post('/category/{country}/', )
async def add_category(country,request:Request, db: Session = Depends(get_db)):
    data = await request.form()

# name: Mapped[str36_unique]
# description: Mapped[str] = mapped_column(Text,nullable=False)
# image: Mapped[image]
    new_category = Category(**data)
    db.add(new_category)
    db.commit()
    return {'data':db.query(Category).all()}

@app.delete('/category/')
def delete_category(request:Request, db: Session = Depends(get_db)):
    return {'data':db.query(Category).order_by(Category.id.desc()).all()}

@app.patch('/category/',)
def update_category(request:Request, db: Session = Depends(get_db)):
    return {'data':db.query(Category).all()}



@app.get('/course')
def get_course(db:Session = Depends(get_db)):
    return {"data":db.query(Course).all()}

@app.get('/task')
def get_task(db:Session = Depends(get_db)):
    return {"data":db.query(Task).all()}

@app.get('/topic')
def get_topic(db:Session = Depends(get_db)):
    return {"data":db.query(Topic).all()}

@app.get('/quiz')
def get_quiz(db:Session = Depends(get_db)):
    return {"data":db.query(Quiz).all()}

@app.get('/quiz_block')
def get_quiz_block(db:Session = Depends(get_db)):
    return {"data":db.query(QuizBlock).all()}

@app.get('/type_quiz')
def get_type_quiz(db:Session = Depends(get_db)):
    return {"data":db.query(TypeQuiz).all()}

@app.get('/answer_user')
def get_answer_user(db:Session = Depends(get_db)):
    return {"data":db.query(AnswerUser).all()}

@app.get('/user')
def get_user(db:Session = Depends(get_db)):
    return {"data":db.query(User).all()}




if __name__ == '__main__':
        #create_db_and_tables()


        uvicorn.run(
            host="127.0.0.1",
            port=8080,
            reload=True,
            app="education_model:app"
        )
