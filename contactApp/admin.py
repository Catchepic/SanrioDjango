# Register your models here.
from .models import Ad
from django.contrib import admin
from .models import Resume
from django.utils.safestring import mark_safe


class ResumeAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'character', 'storeName', 'storeInfo', 'bossName',
                    'bossNum', 'position', 'experience')


admin.site.register(Ad)
admin.site.register(Resume, ResumeAdmin)
