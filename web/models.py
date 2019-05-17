import random
import string

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .templatetags.web_extras import convert_date_to_jalali as to_jalali, convert_digits_to_persian as to_persian


def generate_new_pid(n=12):
    new_pid = None
    prefix_string = 'lmp_'

    while not new_pid:
        postfix_string = ''.join(random.choices(string.ascii_letters + string.digits, k=n))
        new_pid = '%s%s' % (prefix_string, postfix_string)

        if Page.objects.is_pid_exists(new_pid):
            new_pid = None

    return new_pid


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

    def is_pid_exists(self, pid):
        return self.filter(pid=pid).exists()


class Page(models.Model):
    tag = models.ManyToManyField('Tag', verbose_name='برچسب‌ها', related_name='tags', related_query_name='tag',
                                 blank=True)
    pid = models.CharField(_('شناسه‌ی عمومی'), max_length=16, unique=True, default=generate_new_pid)
    title = models.CharField(_('عنوان'), max_length=128)
    subtitle = models.CharField(_('زیرعنوان'), max_length=128, blank=True, default='')
    content = models.TextField(_('محتوا'), max_length=1024)
    event = models.CharField(_('رویداد مهم'), max_length=128, blank=True, default='',
                             help_text='تاریخ یک رویداد مهم برای موضوع وارد شده به همراه محل وقوع.')
    image = models.ImageField(_('تصویر'), upload_to='images', blank=True, default='')
    image_caption = models.CharField(_('توضیح تصویر'), max_length=128, blank=True, default='',
                                     help_text='مکان و موقعیت گرفتن عکس به همراه معرفی افراد حاضر در عکس.')
    reference = models.CharField(_('منبع'), max_length=128, blank=True, default='',
                                 help_text='نام کتاب، روزنامه، مجله یا آدرس سایت، بلاگ و... به همراه نام نویسنده')
    website = models.EmailField(_('وب‌سایت'), max_length=254, blank=True, default='')
    author = models.EmailField(_('ایمیل نویسنده'), max_length=254, blank=True, default='')
    is_active = models.BooleanField(_('فعال'), default=False,
                                    help_text='مشخص می‌کند که این صفحه در لیست نتایج قابل دیدن باشد یا نه.')
    updated_on = models.DateTimeField(_('آخرین به‌روزرسانی'), auto_now=True)
    created_on = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)

    objects = PageManager()

    class Meta:
        verbose_name = 'صفحه'
        verbose_name_plural = 'صفحه'
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def jalali_updated_on(self):
        jalali_date = to_jalali(self.updated_on.strftime('%Y-%m-%d'))
        return to_persian(jalali_date)

    jalali_updated_on.admin_order_field = 'updated_on'
    jalali_updated_on.short_description = 'آخرین به‌روزرسانی'

    def jalali_created_on(self):
        jalali_date = to_jalali(self.created_on.strftime('%Y-%m-%d'))
        return to_persian(jalali_date)

    jalali_created_on.admin_order_field = 'created_on'
    jalali_created_on.short_description = 'تاریخ ایجاد'


class Report(models.Model):
    IS_PENDING = 'pending'
    IS_ACCEPTED = 'accepted'
    IS_DENIED = 'denied'
    STATUS_CHOICES = (
        (IS_PENDING, _('در انتظار')),
        (IS_ACCEPTED, _('نایید شده')),
        (IS_DENIED, _('رد شده')),
    )

    page = models.ForeignKey('Page', to_field='pid', verbose_name='صفحه', on_delete=models.CASCADE)
    body = models.TextField(_('متن گزارش'), max_length=1024)
    reporter = models.EmailField(_('ایمیل گزارش‌دهنده'), max_length=254)
    description = models.TextField(_('توضیحات'), max_length=1024, blank=True, help_text=_(
        'درصورتی که نیاز به یادآوری توضیحاتی در آینده وجود دارد در این قسمت وارد کنید.\
        هم‌چنین در صورت رد گزارش محتوای این فیلد برای کاربر ارسال می‌شود.'))
    status = models.CharField(_('وضعیت رسیدگی'), max_length=32, choices=STATUS_CHOICES, default=IS_PENDING,
                              help_text=_('در تعیین وضیعت رسیدگی دقت کنید. این قسمت تنها یک بار قابل تفییر است.'))
    updated_on = models.DateTimeField(_('آخرین به‌روزرسانی'), auto_now=True)
    created_on = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = 'گزارش'
        verbose_name_plural = 'گزارش'

    def __str__(self):
        return self.page.title

    def jalali_updated_on(self):
        jalali_date = to_jalali(self.updated_on.strftime('%Y-%m-%d'))
        return to_persian(jalali_date)

    jalali_updated_on.admin_order_field = 'updated_on'
    jalali_updated_on.short_description = 'آخرین به‌روزرسانی'

    def jalali_created_on(self):
        jalali_date = to_jalali(self.created_on.strftime('%Y-%m-%d'))
        return to_persian(jalali_date)

    jalali_created_on.admin_order_field = 'created_on'
    jalali_created_on.short_description = 'تاریخ ایجاد'

    def refid(self):
        return f'lmr_{self.page.pid}_{self.pk}'

    refid.short_description = 'شناسه ارجاع'


class Tag(models.Model):
    name = models.CharField(_('نام'), max_length=128, unique=True)
    keyword = models.CharField(_('کلیدواژه'), max_length=128)
    is_active = models.BooleanField(_('فعال'), default=True,
                                    help_text='مشخص می‌کند که این برچسب قابل استفاده باشد یا نه.')
    updated_on = models.DateTimeField(_('آخرین به‌روزرسانی'), auto_now=True)
    created_on = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب'

    def __str__(self):
        return self.name

    def jalali_updated_on(self):
        jalali_date = to_jalali(self.updated_on.strftime('%Y-%m-%d'))
        return to_persian(jalali_date)

    jalali_updated_on.admin_order_field = 'updated_on'
    jalali_updated_on.short_description = 'آخرین به‌روزرسانی'

    def jalali_created_on(self):
        jalali_date = to_jalali(self.created_on.strftime('%Y-%m-%d'))
        return to_persian(jalali_date)

    jalali_created_on.admin_order_field = 'created_on'
    jalali_created_on.short_description = 'تاریخ ایجاد'


class Setting(models.Model):
    SITE_SLOGAN_1 = 'site_slogan_1'
    SITE_SLOGAN_2 = 'site_slogan_2'
    DEFAULT_KEYWORDS = 'default_keywords'
    DEFAULT_DESCRIPTION = 'default_description'
    CONTACT_EMAIL = 'contact_email'
    GOOGLE_ANALYTICS_ID = 'google_analytics_id'
    TYPE_CHOICES = (
        (SITE_SLOGAN_1, _('شعار ۱')),
        (SITE_SLOGAN_2, _('شعار ۲')),
        (DEFAULT_KEYWORDS, _('کلید واژه‌های پیش‌فرض')),
        (DEFAULT_DESCRIPTION, _('توضیح پیش‌فرض')),
        (CONTACT_EMAIL, _('ایمیل ارتباطی')),
        (GOOGLE_ANALYTICS_ID, _('شناسه‌ی Google Analytics'))
    )
    type = models.CharField(_('نوع'), max_length=32, choices=TYPE_CHOICES, unique=True,
                            help_text=_('از هر نوع فقط یک نمونه می‌توانید ایجاد کنید.'))
    content = models.CharField(_('محتوا'), max_length=1024, help_text=_('محتوایی که در سایت نمایش داده می‌شود.'))

    class Meta:
        verbose_name = 'تنظیم'
        verbose_name_plural = 'تنظیمات'

    def __str__(self):
        return self.type
