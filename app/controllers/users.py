from app.common.utils import CustomException
from app.database.models import User
from flask_jwt_extended import create_access_token


class UserControllers(object):

    @staticmethod
    def authenticate(username: str, password: str) -> User:
        users = User.get_all()

        for user in users:
            if username == user.username:
                if user.check_password(password):
                    return user
                else:
                    break
        else:
            raise CustomException('Incorrect user or password', code=400)

    @staticmethod
    def create_user(**kwargs: dict) -> User | None:
        try:
            users = User.get_all()

            for user in users:
                if user.username == kwargs['USERNAME']:
                    raise CustomException('Username already exists', code=406)
                elif user.email == kwargs['EMAIL']:
                    raise CustomException('Email already exists', code=406)

            user = User(**kwargs)
            user.id = len(users) + 1
            user.set_password(kwargs['PASSWORD'])
            user.commit()

            return user
        except CustomException as e:
            raise CustomException(f'{e.message}', code=406)
