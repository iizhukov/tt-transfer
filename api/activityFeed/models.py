from email.policy import default
from unicodedata import category
from django.db import models
from api.authentication.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(
        _('Название'), max_length=64,
    )

    class Meta:
        db_table = "news_category"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return str(self.name)


class News(models.Model):
    title = models.CharField(
        _("Название"), max_length=256,
    )
    body = models.TextField(
        _("Содержимое")
    )
    date = models.DateTimeField(
        _("Дата создания"), default=timezone.now,
    )
    styles = models.JSONField(
        _('Стили'), default=dict, blank=True,
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("автор")
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name=_('Категория'),
        blank=True, null=True,
    )

    class Meta:
        db_table = 'news'
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self) -> str:
        return f"{self.title} : {self.body[:256]}"
