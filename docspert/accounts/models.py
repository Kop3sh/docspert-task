from typing import Iterable
import uuid

from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()

# Create your models here.

class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=False, null=False)
    balance = models.DecimalField(blank=False, default=0, max_digits=10, decimal_places=2)

    def can_withdraw(self, amount: float) -> bool:
        return self.balance >= amount
    
    def __str__(self) -> str:
        return f"id: {self.id}, name: {self.name}, balance: {self.balance}\n"

    def delete(self, *args, **kwargs):
        # Update related Transactions before deleting the Account
        default_account_id = self.id
        Transaction.objects.filter(source_account=self).update(source_account=default_account_id)
        Transaction.objects.filter(destination_account=self).update(destination_account=default_account_id)
        super(Account, self).delete(*args, **kwargs)

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # TODO: ideally, keep the transactions with ids of source and destination accounts, could be implemented with signals
    source = models.ForeignKey("accounts.Account", on_delete=models.CASCADE, related_name="outgoing_transactions")
    destination = models.ForeignKey("accounts.Account", on_delete=models.CASCADE, related_name="icoming_transactions")
    amount = models.DecimalField(blank=False, null=False, max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"source account: {self.source.id}\ndestination account: {self.destination.id}\namount: {self.amount}\n"

    def clean(self):
        if not self.source.can_withdraw(self.amount):
            raise ValidationError('Insufficient funds in the source account for this transaction.')
    
    def save(self, *args, **kwargs):
        self.clean()
        with transaction.atomic():
            self.source.balance -= self.amount
            self.destination.balance += self.amount
            self.source.save()
            self.destination.save()
            super(Transaction, self).save(*args, **kwargs)  # Correct way to call the parent save method