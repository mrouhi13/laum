from django import urls
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from web.models import User, Page, Tag, Report, WebsiteSetting
from web.persian_editors import PersianEditors
from web.utils.email import SendEmail

admin.site.site_header = _('Laum admin panel')
admin.site.site_title = _('Laum admin panel')
admin.site.index_title = _('Dashboard')


@admin.register(User)
class UserAdmin(UserAdmin):
    date_hierarchy = 'date_joined'
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    readonly_fields = ('last_login', 'date_joined')


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    readonly_fields = ['image_tag', 'link_to_page', 'link_to_reports', 'jalali_updated_on', 'jalali_created_on']
    fieldsets = [
        (_('Main info'),
         {'fields': ['link_to_page', 'title', 'subtitle', 'content', 'event', 'image', 'image_tag', 'image_caption']}),
        (_('Further info'), {'fields': ['tags', 'reference', 'website', 'author', 'is_active', 'link_to_reports']}),
        (_('Important dates'), {'fields': ['jalali_updated_on', 'jalali_created_on']})]
    list_display = ['title', 'author', 'is_active', 'jalali_updated_on', 'jalali_created_on']
    list_filter = ['is_active', 'updated_on', 'created_on']
    search_fields = ['title', 'content', 'event', 'image_caption', 'tag__name', 'tag__keyword', 'website', 'author',
                     'reference']
    filter_horizontal = ['tags']

    def link_to_page(self, obj):
        link = urls.reverse(f'web:page-detail', args=[obj.pid])
        return mark_safe(f'<a href="{link}" target="_blank">{obj.pid}</a>')

    link_to_page.short_description = _('public ID')

    def link_to_reports(self, obj):
        reports = obj.reports.all()
        reports_link = []

        for report in reports:
            link = urls.reverse(f'admin:web_report_change', args=[report.pk])
            reports_link.append(f'<a href="{link}" target="_blank">{report.body[:15]}...</a>')
        return mark_safe('، '.join(reports_link))

    link_to_reports.short_description = _('reports')

    def image_tag(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width=150 height=150>')

    image_tag.short_description = _('image preview')

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
        (_('Main info'), {'fields': ['link_to_page', 'refid', 'body', 'link_to_mail', 'description', 'status']}),
        (_('Important dates'), {'fields': ['jalali_updated_on', 'jalali_created_on']})]
    list_display = ['page', 'link_to_mail', 'status', 'jalali_updated_on', 'jalali_created_on', 'refid']
    list_filter = ['status', 'updated_on', 'created_on']
    search_fields = ['page__pid', 'body', 'reporter', 'refid', 'description']

    def link_to_page(self, obj):
        link = urls.reverse(f'admin:web_page_change', args=[obj.page.pk])
        return mark_safe(f'<a href="{link}" target="_blank">{obj.page.title}</a>')

    link_to_page.short_description = _('page')

    def link_to_mail(self, obj):
        return mark_safe(f'<a href="mailto:{obj.reporter}">{obj.reporter}</a>')

    link_to_mail.short_description = _('reporter')

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ['link_to_page', 'body', 'refid', 'link_to_mail', 'jalali_updated_on',
                                'jalali_created_on']

        if not obj.status == Report.STATUS_IS_PENDING:
            self.readonly_fields.extend(['description', 'status'])
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        is_first_change = False

        if 'status' not in self.readonly_fields and not obj.status == Report.STATUS_IS_PENDING:
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
    fieldsets = [(_('Main info'), {'fields': ['name', 'keyword', 'is_active']}),
                 (_('Important dates'), {'fields': ['jalali_updated_on', 'jalali_created_on']})]
    list_display = ['name', 'keyword', 'is_active', 'jalali_updated_on', 'jalali_created_on']
    list_filter = ['is_active', 'updated_on', 'created_on']
    search_fields = ['name', 'keyword']
    prepopulated_fields = {'keyword': ['name']}


@admin.register(WebsiteSetting)
class WebsiteSettingAdmin(admin.ModelAdmin):
    fieldsets = [(_('Main info'), {'fields': ['setting', 'content']})]
    list_display = ['setting', 'content']
    list_filter = ['setting']
    search_fields = ['setting', 'content']
