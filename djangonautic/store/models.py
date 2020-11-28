from django.db import models

# Create your models here.
class AccountType(models.Model):
    icon = models.ImageField(upload_to='accountType/icon', default=None)
    membership_type = models.CharField(max_length=50, blank=False, null=False)
    account_features = models.CharField(max_length=200, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    time_frame = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.membership_type

class Transaction(models.Model):
    membership_type = models.CharField(max_length=20, blank=True, null=False)
    price_of_subscription = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=True)
    subscriber_first_name = models.CharField(max_length=30, blank=True, null=False)
    subscriber_last_name = models.CharField(max_length=30, blank=True, null=False)
    subscriber_email = models.CharField(max_length=5, blank=True, null=False)
    transaction_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=True)
    date_of_transaction = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subscriber_first_name