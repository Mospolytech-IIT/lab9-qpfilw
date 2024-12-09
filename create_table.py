"""Модуль для Части 1. Подключение к базе данных и создание таблиц"""

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    """определение модели таблицы Users"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    posts = relationship("Post", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

    def update_password(self, new_password):
        """обновление пароля пользователя"""
        self.password = new_password

class Post(Base):
    """определение модели таблицы Posts"""
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="posts")

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', user_id={self.user_id})>"

    def update_content(self, new_content):
        """обновление контента поста"""
        self.content = new_content

def create_tables():
    """функция для подключения к бд и создания таблиц"""
    database_url = "postgresql://postgres:12345@localhost:5432/laba9"
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    print("Таблицы созданы успешно!")

if __name__ == "__main__":
    create_tables()
