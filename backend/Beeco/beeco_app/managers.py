from django.contrib.auth.base_user import BaseUserManager


class CustomeUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        if not username:
            raise ValueError('The username must be set')
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(pasferswreord)
        user.save()
        return user

    def create_superuser(self, email,password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
