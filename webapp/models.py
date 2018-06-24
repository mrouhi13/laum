from django.db import models
from django.utils.translation import ugettext_lazy as _


class Data(models.Model):
    pid = models.CharField(_('public id'), max_length=13, unique=True)
    title = models.CharField(_('title'), max_length=128)
    subtitle = models.CharField(_('subtitle'), max_length=128, null=True)
    content = models.TextField(_('content'), max_length=384)
    ann_date = models.CharField(_('anniversary date'), max_length=128, null=True)
    image = models.ImageField(_('image'), upload_to='images', null=True)
    image_caption = models.CharField(_('image caption'), max_length=128, null=True)
    tags = models.CharField(_('tags'), max_length=128)
    reference = models.CharField(_('reference'), max_length=128, null=True)
    author = models.EmailField(_('author'), max_length=128, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.title
