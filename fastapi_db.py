"""Модуль для Части 3. Базовое FastAPI приложение"""

from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql://postgres:12345@localhost:5432/laba9"
engine = create_engine(DATABASE_URL)
metadata = MetaData()
metadata.reflect(bind=engine)
session_maker = sessionmaker(bind=engine)

users_table = metadata.tables['users']
posts_table = metadata.tables['posts']

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_session():
    """создает и возвращает новую сессию"""
    return session_maker()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    """главная страница"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/users", response_class=HTMLResponse)
def list_users(request: Request):
    """все пользователи"""
    session = get_session()
    users = session.execute(users_table.select()).fetchall()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.post("/users/add")
def add_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)):
    """добавление пользователя в бд"""
    session = get_session()
    session.execute(users_table.insert().values(username=username, email=email, password=password))
    session.commit()
    users = session.execute(users_table.select()).fetchall()
    return templates.TemplateResponse(
        "users.html", 
        {
            "request": request,
            "users": users,
            "message": "User added successfully"
        }
    )

@app.get("/users/{user_id}", response_class=HTMLResponse)
def get_user(user_id: int, request: Request):
    """редактирование пользователя по ID"""
    session = get_session()
    user = session.execute(users_table.select().where(users_table.c.id == user_id)).fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user_edit.html", {"request": request, "user": user})

@app.post("/users/{user_id}/update")
def update_user(
    request: Request,
    user_id: int,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)):
    """обновление данных пользователя в бд"""
    session = get_session()
    session.execute(
        users_table.update()
        .where(users_table.c.id == user_id)
        .values(username=username, email=email, password=password)
    )
    session.commit()
    users = session.execute(users_table.select()).fetchall()
    return templates.TemplateResponse(
        "users.html", 
        {
            "request": request,
            "users": users,
            "message": "User updated successfully"
        }
    )

@app.post("/users/{user_id}/delete")
def delete_user(request: Request, user_id: int):
    """удаление пользователя и связынного с ним поста"""
    session = get_session()
    session.execute(posts_table.delete().where(posts_table.c.user_id == user_id))
    session.execute(users_table.delete().where(users_table.c.id == user_id))
    session.commit()
    users = session.execute(users_table.select()).fetchall()
    return templates.TemplateResponse(
        "users.html", 
        {
            "request": request,
            "users": users,
            "message": "User deleted successfully"
        }
    )

@app.get("/posts", response_class=HTMLResponse)
def list_posts(request: Request):
    """список всех постов"""
    session = get_session()
    posts = session.execute(posts_table.select()).fetchall()
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})

@app.post("/posts/add")
def add_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    user_id: int = Form(...)):
    """добавление поста в бд"""
    session = get_session()
    session.execute(posts_table.insert().values(title=title, content=content, user_id=user_id))
    session.commit()
    posts = session.execute(posts_table.select()).fetchall()
    return templates.TemplateResponse(
        "posts.html", 
        {
            "request": request,
            "posts": posts,
            "message": "Post added successfully"
        }
    )

@app.get("/posts/{post_id}", response_class=HTMLResponse)
def get_post(post_id: int, request: Request):
    """страница редактирования поста по ID"""
    session = get_session()
    post = session.execute(posts_table.select().where(posts_table.c.id == post_id)).fetchone()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("post_edit.html", {"request": request, "post": post})

@app.post("/posts/{post_id}/update")
def update_post(request: Request, post_id: int, title: str = Form(...), content: str = Form(...)):
    """обновление данных поста в бд"""
    session = get_session()
    session.execute(
        posts_table.update()
        .where(posts_table.c.id == post_id)
        .values(title=title, content=content)
    )
    session.commit()
    posts = session.execute(posts_table.select()).fetchall()
    return templates.TemplateResponse(
        "posts.html", 
        {
            "request": request,
            "posts": posts,
            "message": "Post updated successfully"
        }
    )

@app.post("/posts/{post_id}/delete")
def delete_post(request: Request, post_id: int):
    """удаление поста из бд"""
    session = get_session()
    session.execute(posts_table.delete().where(posts_table.c.id == post_id))
    session.commit()
    posts = session.execute(posts_table.select()).fetchall()
    return templates.TemplateResponse(
        "posts.html", 
        {
            "request": request,
            "posts": posts,
            "message": "Post deleted successfully"
        }
    )
