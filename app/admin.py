from django.contrib import admin
from .models import Profile,Category,Product,OrderItem,Order,Transaction,Rate,Delivery

# Register your models here.

admin.site.register(Category)
admin.site.register(Delivery)
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Rate)
admin.site.register(Transaction)
# admin.site.register(OrderItem)