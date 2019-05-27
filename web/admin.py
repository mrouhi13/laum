from django import urls
from django.contrib import admin
from django.utils.safestring import mark_safe

from web.models import Page, Tag, Report, Setting
from web.persian_editors import PersianEditors
from web.utils.email import SendEmail

admin.site.site_header = 'پنل مدیریت لام'
admin.site.site_title = 'پنل مدیریت لام'
admin.site.index_title = 'داشبورد'


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    readonly_fields = ['link_to_page', 'link_to_reports', 'jalali_updated_on', 'jalali_created_on']
    fieldsets = [
        ('اطلاعات اصلی',
         {'fields': ['link_to_page', 'title', 'subtitle', 'content', 'event', 'image', 'image_caption']}),
        ('اطلاعات تکمیلی', {'fields': ['tag', 'reference', 'website', 'author', 'is_active', 'link_to_reports']}),
        ('تاریخ‌ها', {'fields': ['jalali_updated_on', 'jalali_created_on']})]
    list_display = ['title', 'author', 'is_active', 'jalali_updated_on', 'jalali_created_on']
    list_filter = ['is_active', 'updated_on', 'created_on']
    search_fields = ['title', 'content', 'event', 'image_caption', 'tag__name', 'tag__keyword', 'website', 'author',
                     'reference']

    def link_to_page(self, obj):
        link = urls.reverse(f'web:page-detail', args=[obj.pid])
        return mark_safe(f'<a href="{link}" target="_blank">{obj.pid}</a>')

    link_to_page.short_description = 'شناسه‌ی عمومی'

    def link_to_reports(self, obj):
        report_set = obj.report_set.all()
        reports_link = []

        for report in report_set:
            link = urls.reverse(f'admin:web_report_change', args=[report.pk])
            reports_link.append(f'<a href="{link}" target="_blank">{report.body[:15]}...</a>')
        return mark_safe('، '.join(reports_link))

    link_to_reports.short_description = 'گزارش‌ها'

    def save_model(self, request, obj, form, change):
        editor = PersianEditors(['space', 'number', 'arabic', 'punctuation_marks'])

        obj.title = editor.run(obj.title)
        obj.subtitle = editor.run(obj.subtitle)
        obj.content = editor.run(obj.content)
        obj.event = editor.run(obj.event)
        obj.image_caption = editor.run(obj.image_caption)

        super(PageAdmin, self).save_model(request, obj, form, change)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    fieldsets = [
        ('اطلاعات اصلی', {'fields': ['link_to_page', 'refid', 'body', 'link_to_mail', 'description', 'status']}),
        ('تاریخ‌ها', {'fields': ['jalali_updated_on', 'jalali_created_on']})]
    list_display = ['page', 'link_to_mail', 'status', 'jalali_updated_on', 'jalali_created_on', 'refid']
    list_filter = ['status', 'updated_on', 'created_on']
    search_fields = ['page__pid', 'body', 'reporter', 'description']

    def link_to_page(self, obj):
        link = urls.reverse(f'admin:web_page_change', args=[obj.page.pk])
        return mark_safe(f'<a href="{link}" target="_blank">{obj.page.title}</a>')

    link_to_page.short_description = 'صفحه'

    def link_to_mail(self, obj):
        return mark_safe(f'<a href="mailto:{obj.reporter}">{obj.reporter}</a>')

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

        editor = PersianEditors(['space'])
        editor.escape_return = False
        obj.body = editor.run(obj.body)

        editor.set_editors(['space', 'number', 'arabic', 'punctuation_marks'])
        editor.escape_return = True
        obj.description = editor.run(obj.description)

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
