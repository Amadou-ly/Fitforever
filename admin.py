from django.contrib import admin
from .models import Items
from .models import Cart
from .models import Contact

from .models import Blog
from django.contrib import admin
from.models import *
# Register your models here.


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'discount', 'category', 'avatar')


admin.site.register(Items, ItemAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'itemname', 'quantity')


admin.site.register(Cart, CartAdmin)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'caption')


admin.site.register(Blog, BlogAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('subject', 'message')


admin.site.register(Contact, ContactAdmin)

admin.site.register(Category)

admin.site.register(SubCategory)

admin.site.register(Users)

admin.site.register(Discount)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'item', 'quantity', 'date', 'status', 'delivery', 'payment', 'address')

admin.site.register(Order, OrderAdmin)


class Different_AddressAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'address_line1', 'address_line2', 'country', 'zipcode')

admin.site.register(Different_Address, Different_AddressAdmin)

class PaytmAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'number')

admin.site.register(Paytm, PaytmAdmin)

class CardAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'name', 'card_no', 'month', 'year')

admin.site.register(Card, CardAdmin)


