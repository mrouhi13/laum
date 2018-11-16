from django import urls
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from web.utils.email import SendEmail
from .models import Page, Tag, Report, Setting

admin.site.site_header = 'پنل مدیریت لام'
admin.site.site_title = 'پنل مدیریت لام'
admin.site.index_title = 'داشبورد'

admin.site.unregister(Group)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    readonly_fields = ['pid', 'jalali_updated_on', 'jalali_created_on']
    fieldsets = [
        ('اطلاعات اصلی', {'fields': ['pid', 'title', 'subtitle', 'content', 'event', 'image', 'image_caption']}),
        ('اطلاعات تکمیلی', {'fields': ['tag', 'reference', 'website', 'author', 'is_active']}),
        ('تاریخ‌ها', {'fields': ['jalali_updated_on', 'jalali_created_on']})]
    list_display = ['title', 'author', 'is_active', 'jalali_updated_on', 'jalali_created_on']
    list_filter = ['is_active', 'updated_on', 'created_on']
    search_fields = ['title', 'content', 'event', 'image_caption', 'tag__name', 'tag__keyword', 'website', 'author',
                     'reference']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    fieldsets = [
        ('اطلاعات اصلی', {'fields': ['link_to_page', 'refid', 'body', 'link_to_mail', 'description', 'status']}),
        ('تاریخ‌ها', {'fields': ['jalali_updated_on', 'jalali_created_on']})]
    list_display = ['page', 'link_to_mail', 'status', 'jalali_updated_on', 'jalali_created_on', 'refid']
    list_filter = ['status', 'updated_on', 'created_on']
    search_fields = ['page', 'body', 'reporter', 'description', 'refid']

    def link_to_page(self, obj):
        link = urls.reverse('admin:web_page_change', args=[obj.page.id])
        return mark_safe('<a href="{}" target="_blank">{}</a>'.format(link, obj.page.title))

    link_to_page.short_description = 'صفحه'

    def link_to_mail(self, obj):
        return mark_safe('<a href="mailto:{}">{}</a>'.format(obj.reporter, obj.reporter))

    link_to_mail.short_description = 'گزارش‌دهنده'

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ['link_to_page', 'body', 'refid', 'link_to_mail', 'jalali_updated_on',
                                'jalali_created_on']

        if not obj.status == Report.IS_PENDING:
            self.readonly_fields.extend(['description', 'status'])
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        is_first_change = False

        if 'status' not in self.readonly_fields and not obj.status == Report.IS_PENDING:
            is_first_change = True

        if is_first_change and not form.cleaned_data['description']:
            obj.description = '-'

        super(ReportAdmin, self).save_model(request, obj, form, change)

        if is_first_change:
            to = obj.reporter
            context = {'report': obj}
            email_template = 'emails/report_result.html'
            SendEmail(request, context, email_template).send([to])


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    readonly_fields = ['jalali_updated_on', 'jalali_created_on']
    fieldsets = [('اطلاعات اصلی', {'fields': ['name', 'keyword', 'is_active']}),
                 ('تاریخ‌ها', {'fields': ['jalali_updated_on', 'jalali_created_on']})]
    list_display = ['name', 'keyword', 'is_active', 'jalali_updated_on', 'jalali_created_on']
    list_filter = ['is_active', 'updated_on', 'created_on']
    search_fields = ['name', 'keyword']
    prepopulated_fields = {'keyword': ['name']}


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    fieldsets = [('اطلاعات اصلی', {'fields': ['type', 'content']})]
    list_display = ['type', 'content']
    list_filter = ['type']
    search_fields = ['type', 'content']
