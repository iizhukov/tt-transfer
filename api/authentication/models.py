from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('почта'), unique=True, null=False, default=None,
    )
    name = models.CharField(
        _('Имя'), max_length=64,
    )
    surname = models.CharField(
        _('Фамилия'), max_length=64,
    )
    patronymic = models.CharField(
        _('Отчество'), max_length=64,
    )
    phone = models.CharField(
        _('Телефон'), max_length=14,
    )
    passport = models.CharField(
        _('Паспорт'), max_length=10,
    )
    
    is_staff = models.BooleanField(_("Сотрудник"), default=False)
    is_active = models.BooleanField(
        _("Активный"), default=True, help_text=_("Включенно, когда акаунт не в бане")
    )
    is_superuser = models.BooleanField(_("Администратор"), default=False)
    date_joined = models.DateTimeField(
        _("Даты регистрации"), default=timezone.now
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
