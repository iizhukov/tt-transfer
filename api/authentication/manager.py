from venv import create
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from api.profile.models import Admin, Manager, Client, Driver


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        if user.role == "a":
            Admin.objects.create(
                user=user
            )
        elif user.role == "m":
            Manager.objects.create(
                user=user
            )
        elif user.role == "c":
            Client.objects.create(
                user=user
            )
        elif user.role == "d":
            Driver.objects.create(
                user=user,
            )

        # match(user.role):
        #     case "a":
        #         Admin.objects.create(
        #             user=user
        #         )
        #     case "m":
        #         Manager.objects.create(
        #             user=user
        #         )
        #     case "c":
        #         Client.objects.create(
        #             user=user
        #         )
        #     case "d":
        #         Driver.objects.create(
        #             user=user,
        #         )

        print(user.role)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'a')

        return self.create_user(email, password, **extra_fields)
