from django.contrib import admin

# Register your models here.
from .models import MyNew


class MyNewAdmin(admin.ModelAdmin):
    style_fields = {'description': 'ueditor'}


admin.site.register(MyNew, MyNewAdmin)
