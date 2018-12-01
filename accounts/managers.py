from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    # def _create_user(self, email, password, **extra_fields):
    #     """
    #     Creates and saves a User with the given email and password.
    #     """
    #     if not email:
    #         raise ValueError('The given email must be set')
    #     extra_fields.setdefault('user_type', 4)
    #     email = self.normalize_email(email)
    #     user = self.model(email=email, **extra_fields)
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        # email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        # extra_fields.setdefault('username', email)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('user_type', 4)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        # extra_fields.setdefault('username', email)
        extra_fields.setdefault('user_type', 0)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')


        return self._create_user(username, password, **extra_fields)