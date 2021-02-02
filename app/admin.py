from django.contrib import admin
from .models import Profile, Comment,Category,Product,OrderItem,Order,Transaction

# Register your models here.

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Transaction)
# admin.site.register(OrderItem)