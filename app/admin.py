from django.contrib import admin
from .models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'summary', 'descr', 'img')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'descr')
    list_filter = ('name', )

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'text', 'category')
    search_fields = ('category',)
    list_filter = ('category', )    

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'summary', 'descr', 'img', 'price', 'category')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'descr')
    list_filter = ('price', )

class CartAdmin(admin.ModelAdmin):
    list_display = ('id','user',)

class RelationCartServiceAdmin(admin.ModelAdmin):
    list_display = ('id','service','cart')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'services', 'number', 'price', 'user')
 
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('name', 'number', 'address', 'password', 'order', 'cart')


admin.site.register(Category, CategoryAdmin)    
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(RelationCartService, RelationCartServiceAdmin)
admin.site.register(Order, OrderAdmin)
# admin.site.register(User, UserAdmin)