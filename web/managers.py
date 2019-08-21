import random

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .helpers import get_active_language


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


class PageManager(models.Manager):

    def all_active(self):
        return self.filter(is_active=True, language=get_active_language())

    def search(self, text):
        vector = SearchVector('title', weight='A') + \
                 SearchVector('subtitle', weight='B') + \
                 SearchVector(StringAgg('tags__name', delimiter=' '),
                              weight='C') + \
                 SearchVector('content', 'event', 'image_caption', weight='D')
        query = SearchQuery(text, search_type='plain')
        rank = SearchRank(vector, query)
        return self.all_active().annotate(
            rank=rank).filter(rank__gte=0.01).order_by('-rank')

    def get_random_pages(self):
        all_pages = self.all_active()
        pages_sample_list = list(all_pages.values_list('pk', flat=True))
        max_random_page_count = 3  # TODO: Make this variable dynamic.

        if len(pages_sample_list) < 3:
            max_random_page_count = len(pages_sample_list)

        random_pages_id = random.sample(pages_sample_list,
                                        max_random_page_count)
        random_pages_list = list(all_pages.filter(pk__in=random_pages_id))

        random.shuffle(random_pages_list)

        return random_pages_list

    def is_pid_exist(self, pid):
        return self.filter(pid=pid).exists()


class GroupManager(models.Manager):

    def is_gid_exist(self, gid):
        return self.filter(gid=gid).exists()
