from .models import Category, Retailer, Transaction, TransactionMethod
from django.contrib import admin

admin.site.register(Category)
admin.site.register(Retailer)
admin.site.register(Transaction)
admin.site.register(TransactionMethod)
