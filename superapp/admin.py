from django.contrib import admin
from .models import *
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import *
from .models import *


admin.site.register(Doctor)

class MyModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'time', 'content']  # указываем поля для отображения в списке
    readonly_fields = ['time']  # указываем поля только для чтения

admin.site.register(Dairy, MyModelAdmin)
admin.site.register(Room)
admin.site.register(Message)