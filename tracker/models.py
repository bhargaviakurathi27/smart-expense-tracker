from django.conf import settings
from django.db import models


class Category(models.Model):
    """A label like Food or Salary. Shared across all users."""
    TYPE_CHOICES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]
    name = models.CharField(max_length=50, unique=True)
    category_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """One income or expense entry owned by a single user."""
    TYPE_CHOICES = Category.TYPE_CHOICES

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="transactions",
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="transactions"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.transaction_type}: {self.amount} ({self.category})"


class Budget(models.Model):
    """A user's spending limit for one month."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="budgets",
    )
    month = models.PositiveSmallIntegerField()  # 1-12
    year = models.PositiveSmallIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "month", "year")  # one budget per user per month

    def __str__(self):
        return f"{self.user} - {self.month}/{self.year}: {self.amount}"