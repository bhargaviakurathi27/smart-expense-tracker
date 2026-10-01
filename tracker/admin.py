from django.contrib import admin
from .models import Category, Transaction, Budget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'created_at']
    list_filter = ['category_type']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'category', 'amount', 'date']
    list_filter = ['transaction_type', 'category', 'date']
    search_fields = ['description', 'user__username']
    ordering = ['-date']
    date_hierarchy = 'date'  # adds a clickable date drill-down at the top


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'month', 'year', 'amount']
    list_filter = ['year', 'month']
    search_fields = ['user__username']
    ordering = ['-year', '-month']