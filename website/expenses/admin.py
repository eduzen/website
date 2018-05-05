# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Expense, Category


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'created_date',
        'amount_currency',
        'amount',
    )
    list_filter = ('created_date',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('name',)
