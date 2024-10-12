from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Subscription
from .models import SubscriptionPlan
from datetime import timedelta
from .models import SubscriptionPlan, Payment
from django.urls import reverse
from django.http import JsonResponse
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@csrf_exempt
def upgrade_to_premium(user):
    premium_plan = get_object_or_404(SubscriptionPlan, plan_name='premium')
    subscription = user.subscription
    subscription.plan = premium_plan
    subscription.start_date = timezone.now()
    subscription.end_date = subscription.start_date + timedelta(days=premium_plan.duration_in_days)
    subscription.save()

@csrf_exempt
def create_payment(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    payment = Payment.objects.create(
        subscriptionplan=plan,
        user=request.user,
        amount=plan.price,
        transaction_id=str(uuid.uuid4()),
        payment_status="pending"
    )
    
    # payment.payment_url = f"http://example.com/pay/{payment.transaction_id}"
    payment.save()

    return JsonResponse({
        'message': 'Payment created successfully',
        'payment_url': payment.payment_url,
        'transaction_id': payment.transaction_id
    })


@csrf_exempt
def confirm_payment(request, transaction_id):
    payment = get_object_or_404(Payment, transaction_id=transaction_id)

    payment.payment_status = "successful"
    payment.save()

    user_subscription = payment.user.subscription
    user_subscription.plan = payment.subscriptionplan
    user_subscription.start_date = timezone.now()
    user_subscription.end_date = user_subscription.start_date + timedelta(days=payment.subscriptionplan.duration_in_days)
    user_subscription.save()

    return JsonResponse({
        'message': 'Payment confirmed and subscription upgraded successfully'
    })