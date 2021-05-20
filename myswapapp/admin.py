from django.contrib import admin

from .models import Product, OrderProduct, Order , Profile, User, Chat, Messages, Address, Basket



class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Chat)
admin.site.register(Messages)
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(User)
admin.site.register(Address)
admin.site.register(Basket)



