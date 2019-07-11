from django.db import models
from djmoney.models.fields import MoneyField
from django.utils import timezone


class Expense(models.Model):
    title = models.CharField(max_length=200, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    Category = models.ForeignKey(
        "expenses.Category", blank=True, null=True, on_delete=models.CASCADE
    )
    amount = MoneyField(max_digits=10, decimal_places=2, default_currency="ARS")

    class Meta:
        verbose_name_plural = "Expenses"

    def __str__(self):
        return f"<Expense: {self.title} - {self.amount}>"


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"<Category: {self.name}>"
