from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Subscription, SubscriptionPlan

@receiver(post_save, sender=User)
def create_default_subscription(sender, instance, created, **kwargs):
    if created:
        try:
            free_plan = SubscriptionPlan.objects.get(plan_name='free')
            Subscription.objects.create(user=instance, plan=free_plan)
        except SubscriptionPlan.DoesNotExist:
            print("Free plan does not exist.")
