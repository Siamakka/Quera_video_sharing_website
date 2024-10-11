from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Subscription
from .models import SubscriptionPlan


def upgrade_to_premium(user):
    premium_plan = get_object_or_404(SubscriptionPlan, plan_name='premium')
    subscription = user.subscription
    subscription.plan = premium_plan
    subscription.start_date = timezone.now()
    subscription.end_date = subscription.start_date + timedelta(days=premium_plan.duration_in_days)
    subscription.save()
