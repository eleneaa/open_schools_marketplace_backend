from users.models import User


class UserService:
    def get_user_by_user_id(self, id: int) -> User:
        if user := User.objects.filter(id=id).first():
            return user

        raise User.DoesNotExist("User with this id does not exist")
