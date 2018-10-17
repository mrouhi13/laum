from django import urls
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from .models import Page, Tag, Report

admin.site.site_header = 'پنل مدیریت لام'
admin.site.site_title = 'پنل مدیریت لام'
admin.site.index_title = 'داشبورد'

admin.site.unregister(Group)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    readonly_fields = ('pid', 'jalali_updated_on', 'jalali_created_on')
    fieldsets = [
        ('اطلاعات اصلی', {'fields': ['pid', 'title', 'subtitle', 'content', 'event', 'image', 'image_caption']}),
        ('اطلاعات تکمیلی', {'fields': ['tag', 'reference', 'website', 'author', 'is_active']}),
        ('تاریخ‌ها', {'fields': ['jalali_updated_on', 'jalali_created_on']})]
    list_display = ('title', 'author', 'is_active', 'jalali_updated_on', 'jalali_created_on')
    list_filter = ['author', 'is_active', 'updated_on', 'created_on']
    search_fields = ['title', 'content', 'event', 'image_caption', 'tag__name', 'tag__keyword', 'website', 'author',
                     'reference']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    readonly_fields = ['link_to_page', 'jalali_updated_on', 'jalali_created_on']
    fieldsets = [('اطلاعات اصلی', {'fields': ['link_to_page', 'body', 'reporter', 'status', 'description']}),
                 ('تاریخ‌ها', {'fields': ['jalali_updated_on', 'jalali_created_on']})]
    list_display = ['page', 'reporter', 'status', 'jalali_updated_on', 'jalali_created_on']
    list_filter = ['reporter', 'status', 'updated_on', 'created_on']
    search_fields = ['page', 'body', 'reporter', 'description']

    def link_to_page(self, obj):
        link = urls.reverse('admin:web_page_change', args=[obj.page.id])
        return mark_safe('<a href="{}" target="_blank">{}</a>'.format(link, obj.page.title))

    link_to_page.short_description = 'صفحه'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    readonly_fields = ('jalali_updated_on', 'jalali_created_on')
    fieldsets = [
        ('اطلاعات اصلی', {'fields': ['name', 'keyword', 'is_active']}),
        ('تاریخ‌ها', {'fields': ['jalali_updated_on', 'jalali_created_on']}),
    ]
    list_display = ('name', 'keyword', 'is_active', 'jalali_updated_on', 'jalali_created_on')
    list_filter = ['is_active', 'updated_on', 'created_on']
    search_fields = ['name', 'keyword']
    prepopulated_fields = {'keyword': ['name']}
