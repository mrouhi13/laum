import random
import string

from django.db import models
from django.utils.translation import ugettext_lazy as _


def generate_new_pid(n=12):
    new_pid_passed = False
    new_pid = ''
    prefix_string = '0'

    while not new_pid_passed:
        postfix_string = ''.join(random.choices(string.ascii_letters + string.digits, k=n))
        new_pid = '%s%s' % (prefix_string, postfix_string)

        if not Data.objects.is_pid_exists(new_pid):
            new_pid_passed = True

    return new_pid


class DataManager(models.Manager):
    def get_random_data(self):
        data_count = self.count()

        if data_count < 3:
            random_data = self.all()
        else:
            random_data = [self.get(id=i) for i in random.sample(range(1, data_count + 1), 3)]

        return random_data

    def is_pid_exists(self, pid):
        return self.filter(pid=pid).exists()


class Data(models.Model):
    tag = models.ManyToManyField('Tag', related_name='tags', related_query_name="tag")
    pid = models.CharField(_('شناسه‌ی عمومی'), max_length=13, unique=True, default=generate_new_pid)
    title = models.CharField(_('عنوان'), max_length=128)
    subtitle = models.CharField(_('زیرعنوان'), max_length=128, blank=True, default='')
    content = models.TextField(_('محتوا'), max_length=1024)
    ann_date = models.CharField(_('تاریخ'), max_length=128, blank=True, default='')
    image = models.ImageField(_('تضویر'), upload_to='images', blank=True, default='')
    image_caption = models.CharField(_('توضیح تصویر'), max_length=128, blank=True, default='')
    reference = models.CharField(_('منبع'), max_length=128, blank=True, default='')
    author = models.EmailField(_('نویسنده'), max_length=254, blank=True, default='')
    status = models.BooleanField(_('وضعیت'), default=False)
    updated_on = models.DateTimeField(_('آخرین به‌روزرسانی'), auto_now=True)
    created_on = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)

    objects = DataManager()

    class Meta:
        verbose_name = "صفحه"
        verbose_name_plural = "صفحه"
        ordering = ['created_on']

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(_('نام'), max_length=128)
    status = models.BooleanField(_('وضعیت'), default=False)
    updated_on = models.DateTimeField(_('آخرین به‌روزرسانی'), auto_now=True)
    created_on = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)

    objects = DataManager()

    class Meta:
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب‌ها"

    def __str__(self):
        return self.name
