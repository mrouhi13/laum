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
            raise ValueError(_('ایمیل وارد نشده است.'))
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
            raise ValueError(_('برای کاربر مدیر is_staff باید فعال باشد.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('برای کاربر مدیر is_superuser باید فعال باشد.'))
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('Email'), unique=True,
                              error_messages={'unique': _('کاربری با این ایمیل وجود دارد.')})

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')


class BaseModel(models.Model):
    updated_on = models.DateTimeField(_('تاریخ به‌روزرسانی'), auto_now=True)
    created_on = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)

    def jalali_updated_on(self):
        jalali_date = to_jalali(self.updated_on.strftime('%Y-%m-%d'))
        return to_persian(jalali_date)

    jalali_updated_on.admin_order_field = 'updated_on'
    jalali_updated_on.short_description = _('تاریخ به‌روزرسانی')

    def jalali_created_on(self):
        jalali_date = to_jalali(self.created_on.strftime('%Y-%m-%d'))
        return to_persian(jalali_date)

    jalali_created_on.admin_order_field = 'created_on'
    jalali_created_on.short_description = _('تاریخ ایجاد')

    class Meta:
        abstract = True


class PageManager(models.Manager):
    def get_random_pages(self):
        page_count = self.count()
        random_page = list()
        all_pages = self.filter(is_active=True)

        if all_pages.count() <= 3:
            random_page = list(all_pages)
        else:
            while len(random_page) < 3:
                remaining_count = 3 - len(random_page)
                random_ids = random.sample(range(1, page_count + 1), remaining_count)

                for i in random_ids:
                    random_page += self.filter(id=i, is_active=True)

                    page_set = set(random_page)
                    random_page = list(page_set)

        random.shuffle(random_page)

        return random_page

    def is_pid_exist(self, pid):
        return self.filter(pid=pid).exists()


class Page(BaseModel):
    tags = models.ManyToManyField('Tag', verbose_name=_('برچسب‌ها'), related_name='tags', related_query_name='tag',
                                  blank=True)
    pid = models.CharField(_('شناسه‌ی عمومی'), max_length=16, unique=True, default=generate_pid, db_index=True)
    title = models.CharField(_('عنوان'), max_length=128, db_index=True)
    subtitle = models.CharField(_('زیرعنوان'), max_length=128, blank=True, db_index=True)
    content = models.TextField(_('محتوا'), max_length=1024, db_index=True)
    event = models.CharField(_('رویداد مهم'), max_length=128, blank=True,
                             help_text=_('تاریخ یک رویداد مهم برای موضوع وارد شده به همراه محل وقوع.'), db_index=True)
    image = models.ImageField(_('تصویر'), upload_to='images', blank=True)
    image_caption = models.CharField(_('توضیح تصویر'), max_length=128, blank=True, db_index=True,
                                     help_text=_('مکان و موقعیت گرفتن عکس به همراه معرفی افراد حاضر در عکس.'))
    reference = models.CharField(_('منبع'), max_length=128, blank=True,
                                 help_text=_('نام کتاب، روزنامه، مجله یا آدرس سایت، بلاگ و... به همراه نام نویسنده'))
    website = models.URLField(_('وب‌سایت'), blank=True)
    author = models.EmailField(_('ایمیل نویسنده'), blank=True)
    is_active = models.BooleanField(_('فعال'), default=False,
                                    help_text=_('مشخص می‌کند که این صفحه در لیست نتایج قابل دیدن باشد یا نه.'))

    objects = PageManager()

    class Meta:
        verbose_name = _('صفحه')
        verbose_name_plural = _('صفحه‌ها')

    def __str__(self):
        return self.title


class Report(BaseModel):
    STATUS_IS_PENDING = 'pending'
    STATUS_IS_ACCEPTED = 'accepted'
    STATUS_IS_DENIED = 'denied'
    STATUS_CHOICES = (
        (STATUS_IS_PENDING, _('در انتظار')),
        (STATUS_IS_ACCEPTED, _('تایید شده')),
        (STATUS_IS_DENIED, _('رد شده')),
    )

    page = models.ForeignKey('Page', to_field='pid', on_delete=models.CASCADE, related_name='reports',
                             verbose_name=_('صفحه'), )
    refid = models.CharField(_('شناسه‌ی ارجاع'), max_length=32, unique=True, null=True)
    body = models.TextField(_('متن گزارش'), max_length=1024)
    reporter = models.EmailField(_('ایمیل گزارش‌دهنده'))
    description = models.TextField(_('توضیحات'), max_length=1024, blank=True, help_text=_(
        'درصورتی که نیاز به یادآوری توضیحاتی در آینده وجود دارد در این قسمت وارد کنید.\
        هم‌چنین در صورت رد گزارش محتوای این فیلد برای کاربر ارسال می‌شود.'))
    status = models.CharField(_('وضعیت رسیدگی'), max_length=32, choices=STATUS_CHOICES, default=STATUS_IS_PENDING,
                              help_text=_('در تعیین وضیعت رسیدگی دقت کنید. این قسمت تنها یک بار قابل تفییر است.'))

    class Meta:
        verbose_name = _('گزارش')
        verbose_name_plural = _('گزارش‌ها')

    def __str__(self):
        return self.page.title


class Tag(BaseModel):
    name = models.CharField(_('نام'), max_length=50, unique=True, db_index=True)
    keyword = models.SlugField(_('کلیدواژه'), allow_unicode=True, db_index=True)
    is_active = models.BooleanField(_('فعال'), default=True,
                                    help_text=_('مشخص می‌کند که این برچسب قابل استفاده باشد یا نه.'))

    class Meta:
        verbose_name = _('برچسب')
        verbose_name_plural = _('برچسب‌ها')

    def __str__(self):
        return self.name


class WebsiteSetting(models.Model):
    SETTING_SITE_SLOGAN_1 = 'site_slogan_1'
    SETTING_SITE_SLOGAN_2 = 'site_slogan_2'
    SETTING_DEFAULT_KEYWORDS = 'default_keywords'
    SETTING_DEFAULT_DESCRIPTION = 'default_description'
    SETTING_CONTACT_EMAIL = 'contact_email'
    SETTING_NOTIFICATION_EMAIL = 'notification_email'
    SETTING_GOOGLE_ANALYTICS_ID = 'google_analytics_id'
    SETTING_CHOICES = (
        (SETTING_SITE_SLOGAN_1, _('شعار ۱')),
        (SETTING_SITE_SLOGAN_2, _('شعار ۲')),
        (SETTING_DEFAULT_KEYWORDS, _('کلید واژه‌های پیش‌فرض')),
        (SETTING_DEFAULT_DESCRIPTION, _('توضیح پیش‌فرض')),
        (SETTING_CONTACT_EMAIL, _('ایمیل ارتباطی')),
        (SETTING_NOTIFICATION_EMAIL, _('ایمیل اطلاع‌رسانی')),
        (SETTING_GOOGLE_ANALYTICS_ID, _('شناسه‌ی Google Analytics'))
    )
    setting = models.CharField(_('تنظیم'), max_length=32, choices=SETTING_CHOICES, unique=True,
                               help_text=_('از هر تنطیم فقط یک نمونه می‌توانید ایجاد کنید.'))
    content = models.CharField(_('محتوا'), max_length=1024, help_text=_('محتوایی که در سایت نمایش داده می‌شود.'))

    class Meta:
        verbose_name = _('تنظیم')
        verbose_name_plural = _('تنظیمات وب سایت')

    def __str__(self):
        return self.setting
