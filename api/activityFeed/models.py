from email.policy import default
from django.db import models
from api.authentication.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


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
        _('Стили'), default=dict,
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("автор")
    )

    class Meta:
        db_table = 'news'
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self) -> str:
        return f"{self.title} : {self.body[:256]}"
