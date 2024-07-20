import importlib
from fastapi import FastAPI
from .views import view_lk, view_quiz, view_user, view_cinema


DEBUG = True


app = FastAPI(debug=DEBUG,)

app.include_router(view_lk.router)
app.include_router(view_quiz.router)
app.include_router(view_user.router)
app.include_router(view_cinema.router)
