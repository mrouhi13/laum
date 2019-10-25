from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from templated_mail.mail import BaseEmailMessage

from .models import User, Group, Page, Tag, Report
from .persian_editors import PersianEditors

admin.site.site_header = _('Laum Project administration')
admin.site.site_title = _('Laum Project administration')
admin.site.index_title = _('Dashboard')


class BaseModelAdmin(admin.ModelAdmin):
    object_tools = ()

    def get_object_tools(self):
        """
        Return a sequence containing the fields to be displayed on the
        changelist.
        """
        return self.object_tools

    def prepare_object_tools(self, obj):
        object_tools_link = {}
        if obj:
            object_tools = self.get_object_tools()
            for object_tool in object_tools:
                callable_obj = getattr(self, object_tool)
                url = callable_obj(obj)
                if url:
                    if hasattr(callable_obj, 'short_description'):
                        object_tools_link.update({
                            callable_obj.short_description: url
                        })
                    else:
                        object_tools_link.update({
                            callable_obj.__str__(): url
                        })
        return object_tools_link

    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        context.update({
            'object_tools': self.prepare_object_tools(obj)
        })
        return super().render_change_form(request, context, add, change,
                                          form_url, obj)

    def get_queryset(self, request):
        return self.model.objects.active_language()


@admin.register(User)
class UserAdmin(UserAdmin):
    date_hierarchy = 'date_joined'
    fieldsets = [
        [None, {'fields': ['email', 'password']}],
        [_('Personal info'), {'fields': ['first_name', 'last_name']}],
        [_('Permissions'), {
            'classes': ['collapse'],
            'fields': ['is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions']
        }],
        [_('Important dates'), {'fields': ['last_login', 'date_joined']}],
    ]
    add_fieldsets = [
        [None, {
            'classes': ['wide'],
            'fields': ['email', 'password1', 'password2'],
        }],
    ]
    list_display = ['email', 'first_name', 'last_name', 'is_staff',
                    'is_superuser', 'is_active']
    search_fields = ['first_name', 'last_name', 'email']
    ordering = []
    readonly_fields = ['last_login', 'date_joined']
    autocomplete_fields = ['groups']


class PageInlineAdmin(admin.TabularInline):
    model = Page
    readonly_fields = ['pid', 'language', 'created_on']
    fields = ['pid', 'language', 'created_on', 'is_active']
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    readonly_fields = ['gid', 'updated_on', 'created_on']
    fieldsets = [
        [_('Main info'), {'fields': ['gid']}],
        [_('Important dates'), {'fields': ['updated_on', 'created_on']}]
    ]
    list_display = ['title', 'updated_on', 'created_on', 'in_use']
    list_filter = ['updated_on', 'created_on']
    search_fields = ['gid', 'pages__pid', 'pages__title']
    inlines = [PageInlineAdmin]

    def in_use(self, obj):
        return bool(obj.pages.all().count())

    in_use.boolean = True
    in_use.short_description = _('In use?')

    def title(self, obj):
        return obj.__str__()

    title.short_description = _('Title')


@admin.register(Page)
class PageAdmin(BaseModelAdmin):
    date_hierarchy = 'created_on'
    readonly_fields = ['pid', 'updated_on', 'created_on']
    fieldsets = [
        [_('Main info'), {
            'fields': ['pid', 'group', 'title', 'subtitle', 'content', 'event',
                       'image', 'image_caption']
        }],
        [_('Further info'), {
            'classes': ['collapse'],
            'fields': ['tags', 'reference', 'website', 'author', 'is_active']
        }],
        [_('Important dates'), {'fields': ['updated_on', 'created_on']}]
    ]
    list_display = ['title', 'author', 'created_on', 'has_group', 'has_image',
                    'is_active']
    list_filter = ['is_active', 'updated_on', 'created_on']
    search_fields = ['group__gid', 'pid', 'title', 'content', 'event',
                     'image_caption', 'tags__name', 'tags__keyword', 'website',
                     'author', 'reference']
    autocomplete_fields = ['group', 'tags']
    object_tools = ['link_to_reports', 'link_to_group']

    def has_group(self, obj):
        return bool(obj.group)

    has_group.boolean = True
    has_group.short_description = _('Has group?')

    def has_image(self, obj):
        return bool(obj.image)

    has_image.boolean = True
    has_image.short_description = _('Has image?')

    def link_to_reports(self, obj):
        return f'{reverse("admin:web_report_changelist")}?q={obj.pid}'

    link_to_reports.short_description = _('View reports')

    def link_to_group(self, obj):
        if obj.group:
            return reverse('admin:web_group_change', args=[obj.group.pk])
        return None

    link_to_group.short_description = _('Go to group')

    def save_model(self, request, obj, form, change):
        editor = PersianEditors(['space', 'number',
                                 'arabic', 'punctuation_marks'])

        obj.title = editor.run(obj.title)
        obj.subtitle = editor.run(obj.subtitle)
        obj.content = editor.run(obj.content)
        obj.event = editor.run(obj.event)
        obj.image_caption = editor.run(obj.image_caption)

        super().save_model(request, obj, form, change)


@admin.register(Report)
class ReportAdmin(BaseModelAdmin):
    date_hierarchy = 'created_on'
    fieldsets = [
        [_('Main info'), {'fields': ['page', 'rid', 'reporter', 'body']}],
        [_('Supervise info'), {'fields': ['description', 'status']}],
        [_('Important dates'), {'fields': ['updated_on', 'created_on']}]
    ]
    list_display = ['page', 'reporter', 'status', 'created_on']
    list_filter = ['status', 'updated_on', 'created_on']
    search_fields = ['page__pid', 'page__title', 'rid', 'body', 'reporter',
                     'rid', 'description']
    object_tools = ['link_to_page', 'send_email']

    def link_to_page(self, obj):
        return reverse('admin:web_page_change', args=[obj.page.pk])

    link_to_page.short_description = _('Go to page')

    def send_email(self, obj):
        return f'mailto:{obj.reporter}'

    send_email.short_description = _('Send email')

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ['page', 'rid', 'body', 'reporter',
                                'updated_on', 'created_on']
        if obj and not obj.status == Report.STATUS_IS_PENDING:
            self.readonly_fields.extend(['description', 'status'])
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        is_first_change = False

        if 'status' not in self.readonly_fields and \
                not obj.status == Report.STATUS_IS_PENDING:
            is_first_change = True

        if is_first_change and not form.cleaned_data['description']:
            obj.description = _('-')

        editor = PersianEditors(
            ['space', 'number', 'arabic', 'punctuation_marks'])
        obj.description = editor.run(obj.description)

        editor.set_editors(['space'])
        editor.escape_return = False
        obj.body = editor.run(obj.body)

        super().save_model(request, obj, form, change)

        if is_first_change:  # Inform user with email
            context = {'report': obj}
            email_template = 'emails/report_result.html'
            message = BaseEmailMessage(request, context, email_template)
            message.send([obj.reporter])

    def has_add_permission(self, request):
        return False


@admin.register(Tag)
class TagAdmin(BaseModelAdmin):
    readonly_fields = ['updated_on', 'created_on']
    fieldsets = [
        [_('Main info'), {'fields': ['name', 'keyword', 'is_active']}],
        [_('Important dates'), {'fields': ['updated_on', 'created_on']}]
    ]
    list_display = ['name', 'keyword', 'in_use', 'is_active', 'created_on']
    list_filter = ['is_active', 'updated_on', 'created_on']
    search_fields = ['name', 'keyword']
    prepopulated_fields = {'keyword': ['name']}
    object_tools = ['link_to_pages']

    def in_use(self, obj):
        return bool(obj.pages.all().count())

    in_use.boolean = True
    in_use.short_description = _('In use?')

    def link_to_pages(self, obj):
        return f'{reverse("admin:web_page_changelist")}?q={obj.name}'

    link_to_pages.short_description = _('Pages')
