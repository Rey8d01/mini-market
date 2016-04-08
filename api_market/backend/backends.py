from .models import User


class ModelBackend(object):
    def authenticate(self, username=None, password=None):
        if username is not None:
            user = User.objects.get(email=username)
            if user and user.check_password(password):
                return user

        return None