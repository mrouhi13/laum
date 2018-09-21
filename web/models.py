import random
import string

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .templatetags.web_extras import convert_date_to_jalali as to_jalali, convert_digits_to_persian as to_persian


def generate_new_pid(n=12):
    new_pid = ''
    prefix_string = 'a'

    while new_pid == '':
        postfix_string = ''.join(random.choices(string.ascii_letters + string.digits, k=n))
        new_pid = '%s%s' % (prefix_string, postfix_string)

        if Data.objects.is_pid_exists(new_pid):
            new_pid = ''

    return new_pid


class DataManager(models.Manager):
    def get_random_data(self):
        data_count = self.count()
        random_data = list()

        if self.filter(is_active=True).count() <= 3:
            random_data = self.filter(is_active=True)
            random_data = list(random_data)
        else:
            while len(random_data) < 3:
                remaining_count = 3 - len(random_data)
                random_ids = random.sample(range(1, data_count + 1), remaining_count)

                for i in random_ids:
                    random_data += self.filter(id=i, is_active=True)

                    data_set = set(random_data)
                    random_data = list(data_set)

        random.shuffle(random_data)

        return random_data

    def is_pid_exists(self, pid):
        return self.filter(pid=pid).exists()


class Data(models.Model):
    tag = models.ManyToManyField('Tag', verbose_name='برچسب‌ها', related_name='tags', related_query_name='tag',
                                 blank=True)
    pid = models.CharField(_('شناسه‌ی عمومی'), max_length=13, unique=True, default=generate_new_pid)
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

    objects = DataManager()

    class Meta:
        verbose_name = 'صفحه'
        verbose_name_plural = 'صفحه‌ها'
        ordering = ['created_on']

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
    STATUS_IS_PENDING = 'pending'
    STATUS_IS_PROCESSED = 'processed'
    STATUS_IS_DENIED = 'denied'
    STATUS_CHOICES = (
        (STATUS_IS_PENDING, _('در انتظار')),
        (STATUS_IS_PROCESSED, _('رسیدگی شده')),
        (STATUS_IS_DENIED, _('رد شده')),
    )

    data = models.ForeignKey('Data', to_field='pid', verbose_name='صفحه', on_delete=models.CASCADE)
    body = models.TextField(_('متن گزارش'), max_length=1024)
    reporter = models.EmailField(_('ایمیل گزارش‌دهنده'), max_length=254)
    status = models.CharField(_('وضعیت رسیدگی'), max_length=32, choices=STATUS_CHOICES, default=STATUS_IS_PENDING)
    description = models.TextField(_('توضیحات'), max_length=1024, blank=True)
    updated_on = models.DateTimeField(_('آخرین به‌روزرسانی'), auto_now=True)
    created_on = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = 'گزارش'
        verbose_name_plural = 'گزارش‌ها'

    def __str__(self):
        return self.data.title

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


class Tag(models.Model):
    name = models.CharField(_('نام'), max_length=128, unique=True)
    keyword = models.CharField(_('کلیدواژه'), max_length=128)
    is_active = models.BooleanField(_('فعال'), default=True,
                                    help_text='مشخص می‌کند که این برچسب قابل استفاده باشد یا نه.')
    updated_on = models.DateTimeField(_('آخرین به‌روزرسانی'), auto_now=True)
    created_on = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)

    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب‌ها'

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
