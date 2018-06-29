import random

from django.db import models
from django.utils.translation import ugettext_lazy as _


class DataManager(models.Manager):
    def get_random_data(self):
        data_count = self.count()

        if data_count < 3:
            random_data = self.all()
        else:
            random_data = [self.get(id=i) for i in random.sample(range(1, data_count + 1), 3)]

        return random_data


class Data(models.Model):
    pid = models.CharField(_('شناسه‌ی عمومی'), max_length=13, unique=True)
    title = models.CharField(_('عنوان'), max_length=128)
    subtitle = models.CharField(_('زیرعنوان'), max_length=128, blank=True)
    content = models.TextField(_('محتوا'), max_length=1024)
    ann_date = models.CharField(_('تاریخ'), max_length=128, blank=True)
    image = models.ImageField(_('تضویر'), upload_to='images', blank=True)
    image_caption = models.CharField(_('توضیح تصویر'), max_length=128, blank=True)
    reference = models.CharField(_('منبع'), max_length=128, blank=True)
    author = models.EmailField(_('نویسنده'), max_length=254, blank=True)
    # status = models.BooleanField(_('status'), default=False)
    updated_on = models.DateTimeField(_('آخرین به‌روزرسانی'), auto_now=True)
    created_on = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)

    objects = DataManager()

    class Meta:
        verbose_name = "صفحه"
        verbose_name_plural = "صفحه"
        ordering = ['created_on']

    def __str__(self):
        return self.title
