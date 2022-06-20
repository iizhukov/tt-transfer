from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class News(models.Model):
    title = models.CharField(verbose_name=_("Название"), max_length=256)
    body = models.TextField(verbose_name=_("Содержимое"))
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("автор")
    )
    creation_date = models.DateTimeField(
        verbose_name=_("Дата создания"), default=timezone.now()
    )

    class Meta:
        db_table = 'news'
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self) -> str:
        return f"{self.title} : {self.body[:256]}"
