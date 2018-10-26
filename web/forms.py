from django import forms
from django.http import Http404

from web.models import Page, Report


class SearchForm(forms.Form):
    q = forms.CharField(label='جست‌وجو', min_length=1, max_length=100)
    q.widget.attrs.update({'class': 'form-control input-search', 'dir': 'auto', 'aria-label': 'جست‌وجو'})


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'subtitle', 'event', 'content', 'image', 'image_caption', 'reference', 'author']

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {'class': 'form-control', 'placeholder': 'جلال‌الدین محمد بلخی',
                                             'min-length': 3, 'pattern': '.{3,64}'}
        self.fields['subtitle'].widget.attrs = {'class': 'form-control', 'placeholder': 'معروف به مولانا',
                                                'pattern': '.{0}|.{3,32}'}
        self.fields['event'].widget.attrs = {'class': 'form-control', 'placeholder': '۵۸۶ - ۶۵۲ خورشیدی زاده‌ی بلخ',
                                             'pattern': '.{0}|.{3,32}',
                                             'aria-describedby': 'eventHelpLine'}
        self.fields['image'].widget.attrs = {'class': 'custom-file-input'}
        self.fields['image_caption'].widget.attrs = {'class': 'form-control',
                                                     'placeholder': 'نگاره‌ای پندارین از مولانا',
                                                     'pattern': '.{0}|.{3,64}',
                                                     'aria-describedby': 'imageCaptionHelpLine'}
        self.fields['content'].widget.attrs = {'class': 'form-control',
                                               'placeholder': 'مولوی زاده‌ی بلخ خوارزمشاهیان (خراسان در ایران بزرگ، \
                                               افغانستان کنونی) یا وخش بود و...',
                                               'pattern': '.{0}|.{3,64}',
                                               'rows': 17, 'min-length': 100, 'maxlength': 1024}
        self.fields['reference'].widget.attrs = {'class': 'form-control',
                                                 'placeholder': 'شرح زندگانی مولوی، به قلم بدیع‌الزمان فروزانفر',
                                                 'pattern': '.{0}|.{3,64}',
                                                 'aria-describedby': 'referenceHelpLine'}
        self.fields['author'].widget.attrs = {'class': 'form-control text-left direction-left',
                                              'placeholder': 'youremail@example.com'}
        self.fields['author'].label = 'ایمیل شما'


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['page', 'body', 'reporter']
        widgets = {'page': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs = {'class': 'form-control',
                                            'placeholder': 'مثال: قسمت توضیحات عکس غلط نگارشی دارد.',
                                            'aria-label': 'جست‌وجو', 'rows': 5, 'minlength': 3, 'maxlength': 102}
        self.fields['reporter'].widget.attrs = {'class': 'form-control text-left direction-left',
                                                'placeholder': 'youremail@example.com'}
        self.fields['reporter'].label = 'ایمیل'

    def clean_page(self):
        page = self.cleaned_data['page']
        if not page.is_active:
            raise Http404
        return page
