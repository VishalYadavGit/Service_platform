from django.contrib import admin
# Register your models here.
from .models import Service
from .models import Product
class AdminProduct(admin.ModelAdmin):
    list_display=('name',)

class AdminService(admin.ModelAdmin):
    list_display=('name',)
    
admin.site.register(Service)
admin.site.register(Product)
