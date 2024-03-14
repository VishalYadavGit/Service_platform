from django.contrib import admin
# Register your models here.
from .models import Service, Booking
class AdminProduct(admin.ModelAdmin):
    list_display=('name',)

class AdminService(admin.ModelAdmin):
    list_display=('name',)
    
admin.site.register(Service)
admin.site.register(Booking)