from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def default_free_subscription_expiry():
    return timezone.now().date() + timedelta(days=30)

class SubscriptionProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='subscription_profile',
        verbose_name='Пользователь'
    )
    free_subscription_expiry = models.DateField(
        default=default_free_subscription_expiry,
        help_text="Дата окончания бесплатной подписки."
    )
    paid_subscription_expiry = models.DateField(
        null=True, blank=True,
        help_text="Дата окончания платной подписки. Пусто, если платная подписка отсутствует."
    )
    money_count = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0.00,
        help_text="Сумма денег, связанная с профилем подписки."
    )

    def __str__(self):
        return f"SubscriptionProfile(id={self.id}, user={self.user.username}, free_expiry={self.free_subscription_expiry}, paid_expiry={self.paid_subscription_expiry}, money_count={self.money_count})"
    
    class Meta:
        verbose_name = "Профиль подписки"
        verbose_name_plural = "Профили подписок"





from datetime import date

class Account(models.Model):
    profile = models.ForeignKey(SubscriptionProfile, on_delete=models.CASCADE , verbose_name='Профиль')  # Привязка к профилю пользователя
    updated = models.IntegerField(default=0)  # Счётчик обновлений
    created = models.DateField(default=date.today)  # Дата создания, по умолчанию - сегодня

    def get_value(self):
        return f'{self.updated + 1}{self.created.strftime("%d%m%Y")}'

    def save(self, *args, **kwargs):
        # Если для профиля на сегодня уже есть запись, обновляем счётчик
        if not self.pk and Account.objects.filter(profile=self.profile, created=date.today()).exists():
            account = Account.objects.get(profile=self.profile, created=date.today())
            account.updated += 1
            account.save()
        else:
            super(Account, self).save(*args, **kwargs)  # Сохраняем запись как обычно
