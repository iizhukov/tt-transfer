from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .manager import UserManager


ROLES = (('a', 'admin'), ('m', 'manager'), ('d', 'driver'), ('c', 'client'))


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
    passport = models.CharField(
        _('Паспорт'), max_length=10, blank=True, null=True,
    )
    role = models.CharField(
        _('Роль'), max_length=1, choices=ROLES, default='c'
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
