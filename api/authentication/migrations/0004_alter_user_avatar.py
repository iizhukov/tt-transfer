# Generated by Django 4.0.6 on 2022-08-01 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_userdocument_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='/avatars/default_avatar.png', upload_to='avatars/', verbose_name='Аватар'),
        ),
    ]
