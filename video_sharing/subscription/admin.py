from django.contrib import admin
from subscription.models import SubscriptionPlan
SubscriptionPlan.objects.create(plan_name='free', price=0, duration_in_days=30)
SubscriptionPlan.objects.create(plan_name='premium', price=9.99, duration_in_days=30)
