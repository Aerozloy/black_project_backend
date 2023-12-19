from database import get_user

# вспоминаем комментарии с пары. Смотрим про sqlalchemy, переходим на нее. Не могу сказать, что этот класс несет в
# себе смысл
class User:
    def fromDB(self, user_id):
        self.__user = get_user(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user[0])
