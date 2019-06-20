from django import forms
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from web.models import Page, Report


class SearchForm(forms.Form):
    q = forms.CharField(label=_('جست‌وجو'), min_length=1, max_length=100)
    q.widget.attrs.update({'class': 'form-control input-search', 'dir': 'auto', 'aria-label': _('جست‌وجو')})

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        initial = getattr(self, 'initial', None)
        if initial:
            self.fields['q'].widget.attrs.update({'class': 'form-control input-search input-search-inline'})


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'subtitle', 'event', 'content', 'image', 'image_caption', 'reference', 'author']

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {'class': 'form-control', 'placeholder': _('جلال‌الدین محمد بلخی'),
                                             'min-length': 3, 'pattern': '.{3,64}'}
        self.fields['subtitle'].widget.attrs = {'class': 'form-control', 'placeholder': _('معروف به مولانا'),
                                                'pattern': '.{0}|.{3,32}'}
        self.fields['event'].widget.attrs = {'class': 'form-control', 'placeholder': _('۵۸۶ - ۶۵۲ خورشیدی زاده‌ی بلخ'),
                                             'pattern': '.{0}|.{3,32}',
                                             'aria-describedby': 'eventHelpLine'}
        self.fields['image'].widget.attrs = {'class': 'custom-file-input'}
        self.fields['image_caption'].widget.attrs = {'class': 'form-control',
                                                     'placeholder': _('نگاره‌ای پندارین از مولانا'),
                                                     'pattern': '.{0}|.{3,64}',
                                                     'aria-describedby': 'imageCaptionHelpLine'}
        self.fields['content'].widget.attrs = {'class': 'form-control',
                                               'placeholder': _('مولوی زاده‌ی بلخ خوارزمشاهیان (خراسان در ایران بزرگ، \
                                               افغانستان کنونی) یا وخش بود و...'),
                                               'pattern': '.{0}|.{3,64}',
                                               'rows': 17, 'min-length': 100, 'maxlength': 1024}
        self.fields['reference'].widget.attrs = {'class': 'form-control',
                                                 'placeholder': _('شرح زندگانی مولوی، به قلم بدیع‌الزمان فروزانفر'),
                                                 'pattern': '.{0}|.{3,64}',
                                                 'aria-describedby': 'referenceHelpLine'}
        self.fields['author'].widget.attrs = {'class': 'form-control text-left direction-left',
                                              'placeholder': _('youremail@example.com')}
        self.fields['author'].label = _('ایمیل شما')


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['page', 'body', 'reporter']
        widgets = {'page': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs = {'class': 'form-control',
                                            'placeholder': _('مثال: قسمت توضیحات عکس غلط نگارشی دارد.'),
                                            'aria-label': _('جست‌وجو'), 'rows': 5, 'minlength': 20, 'maxlength': 1024}
        self.fields['reporter'].widget.attrs = {'class': 'form-control text-left direction-left',
                                                'placeholder': _('youremail@example.com')}
        self.fields['reporter'].label = _('ایمیل')

    def clean_page(self):
        page = self.cleaned_data['page']
        if not page.is_active:
            raise Http404
        return page
