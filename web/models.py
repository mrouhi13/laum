from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .helpers import swap_prefix, id_generator, get_active_lang
from .managers import UserManager, PageManager, GroupManager, ReportManager, \
    TagManager


def generate_gid():
    new_gid = None
    while not new_gid:
        postfix_string = id_generator()
        new_gid = f'{settings.GID_PREFIX}_{postfix_string}'
        if Group.objects.is_gid_exist(new_gid):
            new_gid = None
    return new_gid


def generate_pid():
    new_pid = None
    while not new_pid:
        postfix_string = id_generator()
        new_pid = f'{settings.PID_PREFIX}_{postfix_string}'
        if Page.objects.is_pid_exist(new_pid):
            new_pid = None
    return new_pid


@receiver(post_save, sender='web.Report')
def generate_rid(sender, instance=None, created=False, **kwargs):
    if created:
        instance.rid = swap_prefix(f'{instance.page.pid}_{instance.pk}',
                                   settings.RID_PREFIX)
        instance.save()


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True,
                              error_messages={'unique': _(
                                  'A user with that email already exists.')})

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        full_name = self.get_full_name()
        return full_name if full_name else self.get_username()


class BaseModel(models.Model):
    LANGUAGE_CHOICES = settings.LANGUAGES

    language = models.CharField(_('language'), max_length=7, db_index=True,
                                choices=LANGUAGE_CHOICES,
                                default=get_active_lang)
    updated_on = models.DateTimeField(_('updated on'), auto_now=True)
    created_on = models.DateTimeField(_('created on'), auto_now_add=True)

    class Meta:
        abstract = True


class Group(BaseModel):
    language = None
    gid = models.CharField(_('global ID'), max_length=16, primary_key=True,
                           default=generate_gid, db_index=True, editable=False)

    objects = GroupManager()

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')

    def __str__(self):
        page = self.pages.filter(language=get_active_lang()).first()
        return page.title if page else self.gid


class Page(BaseModel):
    group = models.ForeignKey('Group', verbose_name=_('group'),
                              on_delete=models.CASCADE, related_name='pages',
                              null=True, blank=True)
    tags = models.ManyToManyField('Tag', verbose_name=_('tags'), blank=True,
                                  related_name='pages',
                                  related_query_name='tag')
    pid = models.CharField(_('public ID'), max_length=16, unique=True,
                           default=generate_pid, db_index=True)
    title = models.CharField(_('title'), max_length=128, db_index=True)
    subtitle = models.CharField(_('subtitle'), max_length=128, blank=True,
                                db_index=True)
    content = models.TextField(_('content'), max_length=1024, db_index=True)
    event = models.CharField(_('event'), max_length=128, blank=True,
                             # TODO: Rename this field to `event_date`
                             help_text=_(
                                 'Date of an important event for the subject '
                                 'entered along with the place of '
                                 'occurrence.'), db_index=True)
    image = models.ImageField(_('image'), upload_to='images', blank=True)
    image_caption = models.CharField(_('image caption'), max_length=128,
                                     blank=True, db_index=True, help_text=_(
            'A brief description of the location '
            'and history of the photo.'))
    reference = models.CharField(_('reference'), max_length=128, blank=True,
                                 help_text=_(
                                     'The name of the book, newspaper, '
                                     'magazine or website address, blog '
                                     'and... along with the author\'s name.'))
    website = models.URLField(_('website'), blank=True)
    author = models.EmailField(_('author email'), blank=True)
    is_active = models.BooleanField(_('active status'), default=False,
                                    help_text=_(
                                        'Designate whether this page can '
                                        'include on the result list.'))

    objects = PageManager()

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')
        unique_together = ('group', 'language')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('web:page-detail', args=[self.pid])


class Report(BaseModel):
    STATUS_IS_PENDING = 'pending'
    STATUS_IS_ACCEPTED = 'accepted'
    STATUS_IS_DENIED = 'denied'
    STATUS_CHOICES = (
        (STATUS_IS_PENDING, _('Pending')),
        (STATUS_IS_ACCEPTED, _('Accepted')),
        (STATUS_IS_DENIED, _('Denied')),
    )

    page = models.ForeignKey('Page', to_field='pid', verbose_name=_('page'),
                             on_delete=models.CASCADE, related_name='reports')
    rid = models.CharField(_('reference ID'), max_length=32, unique=True,
                           null=True, editable=False)
    body = models.TextField(_('body'), max_length=1024)
    reporter = models.EmailField(_('reporter email'))
    description = models.TextField(_('description'), max_length=1024,
                                   blank=True, help_text=_(
            'A description if need to remember in the future. '
            'Also, if the report is denied, the content of this field will '
            'be sent to the user.'))
    status = models.CharField(_('status'), max_length=32,
                              choices=STATUS_CHOICES,
                              default=STATUS_IS_PENDING, help_text=_(
            'Be careful when determining the status. '
            'This field only is set once.'))

    objects = ReportManager()

    class Meta:
        verbose_name = _('report')
        verbose_name_plural = _('reports')

    def __str__(self):
        return self.page.title

    def get_absolute_url(self):
        return reverse('web:page-detail', args=[self.page.pid])


class Tag(BaseModel):
    name = models.CharField(_('name'), max_length=20, unique=True,
                            db_index=True)
    keyword = models.SlugField(_('keyword'), allow_unicode=True, db_index=True)
    is_active = models.BooleanField(_('active status'), default=True,
                                    help_text=_(
                                        'Designate whether pages related to '
                                        'this tag can include on the result '
                                        'list.'))

    objects = TagManager()

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name
