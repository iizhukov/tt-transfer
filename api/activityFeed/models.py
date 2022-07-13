from argparse import _MutuallyExclusiveGroup
from email.policy import default
from unicodedata import category
from django.db import models
from api.authentication.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# class Category(models.Model):
#     name = models.CharField(
#         _('Название'), max_length=64,
#     )

#     class Meta:
#         db_table = "news_category"
#         verbose_name = "Категория"
#         verbose_name_plural = "Категории"

#     def __str__(self) -> str:
#         return str(self.name)


# class ImageModel(models.Model):
#     name = models.CharField(
#         _('Кодовое название'), max_length=64,
#     )
#     image = models.ImageField(
#         _('Изображение')
#     )

#     class Meta:
#         db_table = "image"
#         verbose_name = "Изображение"
#         verbose_name_plural = "Изображения"


CATEGORIES = (
    ("all", "Для всех"), ("for_managers", "Для менеджеров"),
    ("for_drivers", "Для водителей"), ("for_clients", "Для клиентов")
)


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
    is_important = models.BooleanField(
        _("Важное сообщение"), default=False,
    )
    # category = models.ForeignKey(
    #     Category, on_delete=models.CASCADE, verbose_name=_('Категория'),
    #     blank=True, null=True,
    # )
    # images = models.ManyToManyField(
    #     ImageModel, 
    # )
    category = models.CharField(
        _('Категория'), choices=CATEGORIES,
        max_length=16, default="all",
    )

    class Meta:
        db_table = 'news'
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self) -> str:
        return f"{self.title} : {self.body[:256]}"
