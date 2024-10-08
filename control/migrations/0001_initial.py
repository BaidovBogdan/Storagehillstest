# Generated by Django 5.0.7 on 2024-08-01 16:36

import control.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('free_subscription_expiry', models.DateField(default=control.models.default_free_subscription_expiry, help_text='Дата окончания бесплатной подписки.')),
                ('paid_subscription_expiry', models.DateField(blank=True, help_text='Дата окончания платной подписки. Пусто, если платная подписка отсутствует.', null=True)),
                ('money_count', models.DecimalField(decimal_places=2, default=0.0, help_text='Сумма денег, связанная с профилем подписки.', max_digits=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='subscription_profile', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль подписки',
                'verbose_name_plural': 'Профили подписок',
            },
        ),
    ]
