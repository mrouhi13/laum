from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Data, Tag, Report


class DataAdmin(admin.ModelAdmin):
    readonly_fields = ('pid', 'jalali_updated_on', 'jalali_created_on')
    fieldsets = [
        ('اطلاعات اصلی', {'fields': ['pid', 'title', 'content', 'event', 'image', 'image_caption']}),
        ('اطلاعات تکمیلی', {'fields': ['tag', 'reference', 'author', 'is_active']}),
        ('تاریخ‌ها', {'fields': ['jalali_updated_on', 'jalali_created_on']}),
    ]
    list_display = ('title', 'author', 'is_active', 'jalali_updated_on', 'jalali_created_on')
    list_filter = ['author', 'is_active', 'updated_on', 'created_on']
    search_fields = ['title', 'content', 'event', 'image_caption', 'tag']


class ReportAdmin(admin.ModelAdmin):
    readonly_fields = ('data', 'jalali_updated_on', 'jalali_created_on')
    fieldsets = [
        ('اطلاعات اصلی', {'fields': ['body', 'reporter', 'status']}),
        ('تاریخ‌ها', {'fields': ['jalali_updated_on', 'jalali_created_on']}),
    ]
    list_display = ('data', 'reporter', 'status', 'jalali_updated_on', 'jalali_created_on')
    list_filter = ['reporter', 'status', 'updated_on', 'created_on']
    search_fields = ['data', 'body', 'reporter']


class TagAdmin(admin.ModelAdmin):
    readonly_fields = ('jalali_updated_on', 'jalali_created_on')
    fieldsets = [
        ('اطلاعات اصلی', {'fields': ['name', 'is_active']}),
        ('تاریخ‌ها', {'fields': ['jalali_updated_on', 'jalali_created_on']}),
    ]
    list_display = ('name', 'is_active', 'jalali_updated_on', 'jalali_created_on')
    list_filter = ['is_active', 'updated_on', 'created_on']
    search_fields = ['name', ]


admin.site.register(Data, DataAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.unregister(Group)

admin.site.site_header = 'مدیریت مایتون'
admin.site.site_title = 'مدیریت مایتون'
admin.site.index_title = 'مدیریت مایتون'
