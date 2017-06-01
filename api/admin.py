from django.contrib import admin

# Register your models here.
from models import User, Category, Product, ProductImage, Service, Appointment


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
