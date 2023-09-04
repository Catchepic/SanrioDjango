from django.contrib import admin

# Register your models here.
from django.contrib import admin

from django.contrib import admin
from .models import Store, StoreImg

admin.site.site_header = 'Sanrio网站后台管理系统'
admin.site.site_title = 'Sanrio网站后台管理系统'

class StoreImgInline(admin.StackedInline): #内联模型管理器
    model = StoreImg   #以集成方式在后台显示
    extra = 1     # 默认显示条目的数量

class StoreAdmin(admin.ModelAdmin):  #产品模型管理器
    inlines = [StoreImgInline,]   #内联属性

admin.site.register(Store, StoreAdmin)  #绑定产品模型和产品模型管理器

