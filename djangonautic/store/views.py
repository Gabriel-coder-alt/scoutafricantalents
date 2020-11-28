from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.utils import timezone
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from .models import AccountType

# Create your views here.
def StoreFront(request):
    memberships = AccountType.objects.all()
    return render(request, 'Pricing.html', {'memberships':memberships})

def Checkout(request, id):
    membership = AccountType.objects.get(id=id)
    today = timezone.now()
    membership_plan = membership.membership_type
    price = membership.price
    billing_cycle = 1
    billing_cycle_unit = membership.time_frame
  
    # What you want the button to do.
    paypal_dict = {
        "cmd": "_xclick-subscriptions",
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "a3": price,
        "p3": billing_cycle,  # duration of each unit (depends on unit)
        "t3": billing_cycle_unit,  # duration unit ("M for Month")
        "src": "1",  # make payments recur
        "sra": "1",  # reattempt payment on payment error
        "no_note": "1",  # remove extra notes (optional)
        'item_name': membership_plan,
        'custom': membership.id,     # custom data, pass something meaningful here
        'currency_code': 'USD',
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment_successful')),
        "cancel_return": request.build_absolute_uri(reverse('payment_not_successful')),
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
    return render(request, 'checkout_page.html', {'membership':membership, 'today':today, 'form':form})

@csrf_exempt
def PaymentSuccessful(request):
    return render(request, 'store/payment_successful.html')

@csrf_exempt
def PaymentNotSuccessful(request):
    return render(request, 'store/payment_not_successful.html')