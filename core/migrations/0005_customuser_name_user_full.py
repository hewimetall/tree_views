# Generated by Django 3.2 on 2021-04-27 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_customuser_work'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='name_user_full',
            field=models.CharField(default='test', max_length=12, verbose_name='Полное имя'),
            preserve_default=False,
        ),
    ]
