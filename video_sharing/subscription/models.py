from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta


class SubscriptionPlan(models.Model):
    PLAN_CHOICES = (
        ('free', 'Free'),
        ('premium', 'Premium'),
    )

    plan_name = models.CharField(max_length=50, choices=PLAN_CHOICES, default='free')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    duration_in_days = models.IntegerField(default=30)

    def __str__(self):
        return self.plan_name


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.plan.plan_name}"

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_in_days)
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        return self.end_date >= timezone.now()
