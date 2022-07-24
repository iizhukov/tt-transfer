from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.utils.deconstruct import deconstructible
import os

from api.authentication.models import User


@deconstructible
class UploadImageTo:
    def __call__(self, instance, filename):
        path = os.path.join(settings.MEDIA_ROOT, "news/images/", instance.id)
        return os.path.join(path, filename)


@deconstructible
class UploadFileTo:
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        path = os.path.join(settings.MEDIA_ROOT, "news/files/", instance.id)
        return os.path.join(path, filename)


# def upload_to(prefix):
#     def _path(instance, filename):
#         format = filename.split(".")[-1]
#         path = os.path.join(settings.MEDIA_ROOT, prefix, instance.id)

#         return os.path.join(path, filename)
#     return _path


def upload_images_to(instance, filename):
    path = os.path.join(settings.MEDIA_ROOT, "news/images/", str(instance.news.id))
    return os.path.join(path, filename)


def upload_files_to(instance, filename):
    path = os.path.join(settings.MEDIA_ROOT, "news/files/", str(instance.news.id))
    return os.path.join(path, filename)


class ImageModel(models.Model):
    image = models.ImageField(
        _('Изображение'),
        upload_to=upload_images_to,
    )
    news = models.ForeignKey(
        "News", models.CASCADE,
        default=None
    )

    class Meta:
        db_table = "news_image"
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def __str__(self) -> str:
        return f"{self.news.title}: {self.pk}"

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def save_image_to_client(self):
        path = settings.PROJECT_URL
        client_path = os.path.join(path, f"client/public/uploads/news/images/{self.news.id}/")

        if not os.path.exists(client_path):
            os.mkdir(client_path)

        image = self.image
        filename = str(image)

        with open(os.path.join(client_path, filename), "wb") as img:
            img.write(image.read())


class FileModel(models.Model):
    file = models.FileField(
        _('Изображение'),
        upload_to=upload_files_to,
    )
    news = models.ForeignKey(
        "News", models.CASCADE,
        default=None
    )

    class Meta:
        db_table = "news_file"
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    def __str__(self) -> str:
        return f"{self.news.title}: {self.pk}"

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def save_file_to_client(self):
        path = settings.PROJECT_URL
        client_path = os.path.join(path, f"client/public/uploads/news/files/{self.news.id}/")

        if not os.path.exists(client_path):
            os.mkdir(client_path)

        file = self.file
        filename = str(file)

        with open(os.path.join(client_path, filename), "wb") as fl:
            fl.write(file.read())


CATEGORIES = (
    ("for_all", "Для всех"), ("for_managers", "Для менеджеров"),
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
    category = models.CharField(
        _('Категория'), choices=CATEGORIES,
        max_length=16, default=_("for_all"),
    )

    class Meta:
        db_table = 'news'
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self) -> str:
        return f"{self.title} : {self.body[:256]}"
