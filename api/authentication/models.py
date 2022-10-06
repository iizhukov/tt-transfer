from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.conf import settings
import os

from .manager import UserManager


# @deconstructible
# class UploadAvatarTo:
#     def __init__(self, sub_path):
#         self.path = sub_path

#     def __call__(self, instance, filename):
#         format = filename.split(".")[-1]
#         path = os.path.join(settings.MEDIA_ROOT, "users/", instance.email)

#         print(path)

#         for file in os.listdir(path):
#             if "avatar" in file:
#                 os.remove(os.path.join(path, file))

#         return os.path.join(path, f"avatar.{format}")


def _document_path(instance, filename):
    path = os.path.join(settings.MEDIA_ROOT, "documents/", instance.user.email)

    return os.path.join(path, filename)


def _path(instance, filename):
    format_ = filename.split(".")[-1]
    path = os.path.join("/avatars/", instance.email)

    if os.path.exists(path):
        for file in os.listdir(path):
            if "avatar" in file:
                os.remove(os.path.join(path, file))

    print(os.path.join(path, f"avatar.{format_}"))

    return os.path.join(path, f"avatar.{format_}")


ROLES = (('a', 'admin'), ('m', 'manager'), ('d', 'driver'), ('c', 'client'), ('e', 'employee'))


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('почта'), unique=True, null=False,
    )
    name = models.CharField(
        _('Имя'), max_length=64, blank=True, null=True,
    )
    surname = models.CharField(
        _('Фамилия'), max_length=64, blank=True, null=True,
    )
    patronymic = models.CharField(
        _('Отчество'), max_length=64, blank=True, null=True,
    )
    phone = models.CharField(
        _('Телефон'), max_length=14, blank=True, null=True,
    )
    role = models.CharField(
        _('Роль'), max_length=1, choices=ROLES, default='c'
    )
    confirmed = models.BooleanField(
        _('Подтвержден'), default=False,
    )
    avatar = models.ImageField(
        _('Аватар'), upload_to="avatars/",
        default="/avatars/default_avatar.png"
    )
    is_online = models.BooleanField(
        _('Онлайн'), default=False
    )

    is_staff = models.BooleanField(_("Сотрудник"), default=False)
    is_active = models.BooleanField(
        _("Активный"), default=True, help_text=_("Включено, когда аккаунт не в бане")
    )
    is_superuser = models.BooleanField(_("Администратор"), default=False)
    date_joined = models.DateTimeField(
        _("Дата регистрации"), default=timezone.now
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"

    def save(self, *args, **kwargs):
        if self.role in ("c", "d", "e"):
            self.confirmed = True

        return super(User, self).save(*args, **kwargs)


class ResetPasswordCode(models.Model):
    code = models.IntegerField(
        _('Код авторизации'),
    )
    user = models.ForeignKey(
        User, models.CASCADE, verbose_name=_('Пользователь'),
    )
    end_datetime = models.DateTimeField(
        _('Дата окончания действия'),
    )

    objects = models.Manager()

    class Meta:
        db_table = "reset_password_code"
        verbose_name = "Код сброса пароля"
        verbose_name_plural = "Коды сброса пролей"

    def __str__(self) -> str:
        return f"{self.user.email} : {self.code}"


class UserDocument(models.Model):
    user = models.ForeignKey(
        User, models.CASCADE,
        verbose_name=_('Пользователь')
    )
    document = models.FileField(
        _('Документ'), upload_to="documents/"
    )

    objects = models.Manager()

    class Meta:
        db_table = "user_document"
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self) -> str:
        return f"{self.user} : {self.document}"
