from django.db import models
from django.utils.translation import gettext_lazy as _


# class CarClass(models.Model):
#     name = models.CharField(
#         _("Название"), max_length=64,
#     )

#     class Meta:
#         db_table = "car_class"
#         verbose_name = "Класс автомобиля"
#         verbose_name_plural = "Классы автомобилей"
    
#     def __str__(self) -> str:
#         return str(self.name)


CAR_CLASSES = (
    ('business', 'Бизнес'),
    ('standart', 'Стандарт'),
    ('representative', 'Представительский'),
    ('minivan', 'Минивен'),
    ('minibus', 'Микроавтобус'),
    ('comfort', 'Комфорт'),
    ('bus', 'Автобус'),
    ('business_plus', 'Бизнес плюс'),
    ('cargo', 'Грузовой')
)

CAR_STATUSES = (
    ('main', 'Основной'),
    ('spare', 'Запасной')
)


class Car(models.Model):
    user = models.ForeignKey(
        "authentication.User", models.CASCADE, verbose_name=_('Пользователь'),
        default=None, blank=True
    )
    brand = models.CharField(
        _("Марка"), max_length=64,
    )
    model = models.CharField(
        _('Модель'), max_length=128,
    )
    license_plate = models.CharField(
        _("Номер"), max_length=10,
    )
    power = models.IntegerField(_('Мощность'))
    engine_capacity = models.FloatField(_('Объем двигателя'))
    color = models.CharField(
        _('Цвет'), max_length=32,
    )
    sts = models.CharField(
        _('СТС'), max_length=10,
    )
    pts = models.CharField(
        _('ПТС'), max_length=15,
    )
    car_class = models.CharField(
        _("Класс"), choices=CAR_CLASSES, max_length=24,
    )
    status = models.CharField(
        _('Статус автомобиля'), choices=CAR_STATUSES, max_length=12,
        default="spare"
    )

    class Meta:
        db_table = "car"
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
    
    def __str__(self) -> str:
        return f"{self.brand} {self.model}"

    def set_main_car(self):
        Car.objects.filter(
            user=self.user
        ).update(
            status="spare"
        )

        self.status = "main"
        self.save()
        return self.status
