from app.common.utils import CustomException
from app.database.models import User
from flask_jwt_extended import create_access_token
from app.database import engine


class UserControllers(object):

    @staticmethod
    def authenticate(username: str, password: str) -> User:
        query = engine.execute(
            f""" SELECT * FROM USERS WHERE USERNAME = '{username}' OR EMAIL = '{username}' """).first()

        user = User.get_by_id(query[0])

        if user and user.check_password(password):
            return user
        else:
            raise CustomException('Incorrect user or password', code=400)

    @staticmethod
    def create_user(**kwargs: dict) -> User | None:
        try:
            username: str = kwargs.get('USERNAME')
            email: str = kwargs.get('EMAIL')

            user: User = engine.execute(f""" 
                SELECT * FROM USERS 
                WHERE USERNAME = '{username}'
                AND email = '{email}' 
            """).first()

            if user:
                if user.username == username:
                    raise CustomException('Username already exists', code=406)
                elif user.email == email:
                    raise CustomException('Email already exists', code=406)
            else:
                users = User.get_all()
                new_user = User(**kwargs)

                new_user.id = len(users) + 1
                new_user.set_password(kwargs['PASSWORD'])
                new_user.commit()

            return new_user
        except CustomException as e:
            raise CustomException(f'{e.message}', code=406)
