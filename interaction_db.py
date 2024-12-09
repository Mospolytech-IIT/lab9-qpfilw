"""Модуль для Части 2: создание, добавление, извлечение, обновление и удаление данных"""

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker

def create_tables():
    """ф-ия для подключения к бд и создания таблиц"""
    database_url = "postgresql://postgres:12345@localhost:5432/laba9"
    engine = create_engine(database_url)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    print("Таблицы созданы успешно!")

def get_session():
    """ф-ия для создания сессии"""
    database_url = "postgresql://postgres:12345@localhost:5432/laba9"
    engine = create_engine(database_url)
    session_maker = sessionmaker(bind=engine)
    return session_maker(), engine

def reset_users_sequence():
    """сброс последовательности автоинкремента для таблицы users"""
    session, _ = get_session()
    session.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1;"))
    session.commit()
    print("Последовательность автоинкремента для users сброшена.")

def add_users():
    """добавление данных в таблицу Users"""
    session, _ = get_session()
    metadata = MetaData()
    metadata.reflect(bind=session.bind)
    users_table = metadata.tables['users']

    session.execute(users_table.insert(), [
        {'username': 'user1', 'email': 'user1@example.com', 'password': 'pass1'},
        {'username': 'user2', 'email': 'user2@example.com', 'password': 'pass2'},
        {'username': 'user3', 'email': 'user3@example.com', 'password': 'pass3'},
    ])
    session.commit()
    print("Пользователи добавлены.")

def add_posts():
    """добавление данных в таблицу Posts"""
    session, _ = get_session()
    metadata = MetaData()
    metadata.reflect(bind=session.bind)
    posts_table = metadata.tables['posts']
    users_table = metadata.tables['users']

    user_ids = session.execute(users_table.select()).fetchall()
    user_id_mapping = {user[1]: user[0] for user in user_ids}

    posts = [
        {'title': 'First Post', 'content': 'Content of the first post', \
         'user_id': user_id_mapping.get('user1')},
        {'title': 'Second Post', 'content': 'Content of the second post', \
         'user_id': user_id_mapping.get('user1')},
        {'title': 'Third Post', 'content': 'Content of the third post', \
         'user_id': user_id_mapping.get('user2')},
    ]

    for post in posts:
        if post['user_id'] is not None:
            session.execute(posts_table.insert(), [post])
        else:
            print(f"Ошибка: Пользователь для поста {post['title']} не найден. Пост не добавлен.")
    session.commit()
    print("Посты добавлены.")

def fetch_users():
    """извлечение всех пользователей"""
    session, _ = get_session()
    metadata = MetaData()
    metadata.reflect(bind=session.bind)
    users_table = metadata.tables['users']

    result = session.execute(users_table.select())
    for row in result:
        print(row)

def fetch_posts():
    """извлечение всех постов с пользователями"""
    session, _ = get_session()
    metadata = MetaData()
    metadata.reflect(bind=session.bind)
    posts_table = metadata.tables['posts']

    result = session.execute(posts_table.select())
    for row in result:
        print(row)

def update_user_email(user_id, new_email):
    """обновление email пользователя"""
    session, _ = get_session()
    metadata = MetaData()
    metadata.reflect(bind=session.bind)
    users_table = metadata.tables['users']

    session.execute(users_table.update().where(users_table.c.id == user_id).values(email=new_email))
    session.commit()
    print(f"Email пользователя {user_id} обновлен.")

def update_post_content(post_id, new_content):
    """обновление контента поста"""
    session, _ = get_session()
    metadata = MetaData()
    metadata.reflect(bind=session.bind)
    posts_table = metadata.tables['posts']

    session.execute(
        posts_table.update()
        .where(posts_table.c.id == post_id)
        .values(content=new_content)
    )
    session.commit()
    print(f"Контент поста {post_id} обновлен.")

def delete_post(post_id):
    """удаление поста"""
    session, _ = get_session()
    metadata = MetaData()
    metadata.reflect(bind=session.bind)
    posts_table = metadata.tables['posts']

    session.execute(posts_table.delete().where(posts_table.c.id == post_id))
    session.commit()
    print(f"Пост {post_id} удален.")

def delete_user_and_posts(user_id):
    """удаление пользователя и его постов"""
    session, _ = get_session()
    metadata = MetaData()
    metadata.reflect(bind=session.bind)
    users_table = metadata.tables['users']
    posts_table = metadata.tables['posts']

    session.execute(posts_table.delete().where(posts_table.c.user_id == user_id))
    session.execute(users_table.delete().where(users_table.c.id == user_id))
    session.commit()
    print(f"Пользователь {user_id} и его посты удалены.")

if __name__ == "__main__":
    create_tables()
    reset_users_sequence()
    add_users()
    add_posts()
    fetch_users()
    fetch_posts()
    update_user_email(1, "new_user1@example.com")
    update_post_content(1, "Updated content for the first post")
    delete_post(2)
    delete_user_and_posts(3)
