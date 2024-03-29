from django.contrib import admin
from .models import User,Theaters

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'full_name', 'phone', 'address', 'city', 'state', 'country']

@admin.register(Theaters)
class TheatersAdmin(admin.ModelAdmin):
    list_display = ['id','name','address','city','state','country','capacity']


