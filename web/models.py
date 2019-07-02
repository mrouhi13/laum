import random
import string

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from .helpers import swap_prefix
from .templatetags.web_extras import convert_date_to_jalali as to_jalali, convert_digits_to_persian as to_persian


def generate_pid(n=12):
    new_pid = None

    while not new_pid:
        postfix_string = ''.join(random.choices(string.ascii_letters + string.digits, k=n))
        new_pid = f'{settings.PID_PREFIX}_{postfix_string}'

        if Page.objects.is_pid_exist(new_pid):
            new_pid = None

    return new_pid


@receiver(post_save, sender='web.Report')
def generate_refid(sender, instance=None, created=False, **kwargs):
    if created:
        instance.refid = swap_prefix(f'{instance.page.pid}_{instance.pk}', settings.REFID_PREFIX)
        instance.save()


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_('The given email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True,
                              error_messages={'unique': _('A user with that email already exists.')})

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class BaseModel(models.Model):
    updated_on = models.DateTimeField(_('updated on'), auto_now=True)
    created_on = models.DateTimeField(_('created on'), auto_now_add=True)

    def jalali_updated_on(self):
        jalali_date = to_jalali(self.updated_on.strftime('%Y-%m-%d'))
        return to_persian(jalali_date)

    jalali_updated_on.admin_order_field = 'updated_on'
    jalali_updated_on.short_description = _('updated on')

    def jalali_created_on(self):
        jalali_date = to_jalali(self.created_on.strftime('%Y-%m-%d'))
        return to_persian(jalali_date)

    jalali_created_on.admin_order_field = 'created_on'
    jalali_created_on.short_description = _('created on')

    class Meta:
        abstract = True


class PageManager(models.Manager):
    def get_random_pages(self):
        all_pages = self.filter(is_active=True)
        pages_sample_list = list(all_pages.values_list('pk', flat=True))
        max_random_page_count = 3

        if len(pages_sample_list) < 3:
            max_random_page_count = len(pages_sample_list)

        random_pages_id = random.sample(pages_sample_list, max_random_page_count)
        random_pages_list = list(all_pages.filter(pk__in=random_pages_id))

        random.shuffle(random_pages_list)

        return random_pages_list

    def is_pid_exist(self, pid):
        return self.filter(pid=pid).exists()


class Page(BaseModel):
    tags = models.ManyToManyField('Tag', verbose_name=_('tags'), related_name='tags',
                                  related_query_name='tag', blank=True)
    pid = models.CharField(_('public ID'), max_length=16, unique=True,
                           default=generate_pid, db_index=True)
    title = models.CharField(_('title'), max_length=128, db_index=True)
    subtitle = models.CharField(_('subtitle'), max_length=128, blank=True, db_index=True)
    content = models.TextField(_('content'), max_length=1024, db_index=True)
    event = models.CharField(_('event'), max_length=128, blank=True,
                             help_text=_('Date of an important event for the subject '
                                         'entered along with the place of occurrence.'), db_index=True)
    image = models.ImageField(_('image'), upload_to='images', blank=True)
    image_caption = models.CharField(_('image caption'), max_length=128, blank=True,
                                     db_index=True, help_text=_('A brief description of the location '
                                                                'and history of the photo.'))
    reference = models.CharField(_('reference'), max_length=128, blank=True,
                                 help_text=_('The name of the book, newspaper, magazine '
                                             'or website address, blog and ... along with the author\'s name.'))
    website = models.URLField(_('website'), blank=True)
    author = models.EmailField(_('author email'), blank=True)
    is_active = models.BooleanField(_('active status'), default=False,
                                    help_text=_('Designate whether the page is visible on the list of results.'))

    objects = PageManager()

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')

    def __str__(self):
        return self.title


class Report(BaseModel):
    STATUS_IS_PENDING = 'pending'
    STATUS_IS_ACCEPTED = 'accepted'
    STATUS_IS_DENIED = 'denied'
    STATUS_CHOICES = (
        (STATUS_IS_PENDING, _('Pending')),
        (STATUS_IS_ACCEPTED, _('Accepted')),
        (STATUS_IS_DENIED, _('Denied')),
    )

    page = models.ForeignKey('Page', to_field='pid', on_delete=models.CASCADE,
                             related_name='reports', verbose_name=_('page'))
    refid = models.CharField(_('reference ID'), max_length=32, unique=True, null=True)
    body = models.TextField(_('body'), max_length=1024)
    reporter = models.EmailField(_('reporter email'))
    description = models.TextField(_('description'), max_length=1024, blank=True,
                                   help_text=_('A description if need to recall in the future. '
                                               'Also, if the report is denied, the content of this field will '
                                               'be sent to the user.'))
    status = models.CharField(_('status'), max_length=32, choices=STATUS_CHOICES,
                              default=STATUS_IS_PENDING, help_text=_('Be careful when determining the status. '
                                                                     'This field only is set once.'))

    class Meta:
        verbose_name = _('report')
        verbose_name_plural = _('reports')

    def __str__(self):
        return self.page.title


class Tag(BaseModel):
    name = models.CharField(_('name'), max_length=50, unique=True, db_index=True)
    keyword = models.SlugField(_('keyword'), allow_unicode=True, db_index=True)
    is_active = models.BooleanField(_('active status'), default=True,
                                    help_text=_('Designate whether the tag can be used.'))

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name
