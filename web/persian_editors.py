import re


class PersianEditors(object):
    _persian_punctuation_marks = ['!', '؟', '،', '»', ':', '؛', '.']
    original_text = None
    strip = True
    escape_return = True

    def __setattr__(self, key, value):
        if key in ['_persian_punctuation_marks']:
            raise AttributeError(
                "%s is an immutable attribute." % key
            )
        else:
            super().__setattr__(key, value)

    def __init__(self, editors):
        self._editing_text = None
        self._edited_text = None
        self._editors = None
        self.set_editors(editors)

    def _general_editor(self):
        if self._editing_text is None:
            raise AssertionError(
                'Can\'t access directly to editors, '
                'You must set editors attr then call `.run()`.'
            )

        editing_text = self._editing_text

        if self.strip:
            editing_text = editing_text.strip()

        if self.escape_return:
            editing_text = editing_text.replace('\r', ' ')
            editing_text = editing_text.replace('\n', ' ')

        self._editing_text = editing_text

    def space_editor(self):
        if self._editing_text is None:
            raise AssertionError(
                'Can\'t access directly to editors, '
                'You must set editors attr then call `.run()`.'
            )

        editing_text = self._editing_text
        punctuation_edited = ''

        # Remove space sequence
        while '  ' in editing_text:
            editing_text = editing_text.replace('  ', ' ')

        # Edit space after/before punctuation marks
        for i, char in enumerate(editing_text):
            if char in self._persian_punctuation_marks:
                if editing_text[i - 1] == ' ':
                    punctuation_edited = punctuation_edited[:-1]

                try:
                    if editing_text[i + 1] != ' ' and \
                            editing_text[
                                i + 1] not in self._persian_punctuation_marks:
                        char = f'{char} '
                except IndexError:
                    pass

            if editing_text[i - 1] != ' ' and char == '«':
                char = f' {char}'

            if char == ' ' and editing_text[i - 1] == '«':
                char = ''

            punctuation_edited += char

        self._editing_text = punctuation_edited

    def arabic_editor(self):
        if self._editing_text is None:
            raise AssertionError(
                'Can\'t access directly to editors, '
                'You must set editors attr then call `.run()`.'
            )

        editing_text = self._editing_text

        # Replace 'ي' with 'ی'
        while 'ي' in editing_text:
            editing_text = editing_text.replace('ي', 'ی')

        # Replace 'ك' with 'ک'
        while 'ك' in editing_text:
            editing_text = editing_text.replace('ك', 'ک')

        self._editing_text = editing_text

    def number_editor(self):
        if self._editing_text is None:
            raise AssertionError(
                'Can\'t access directly to editors, '
                'You must set editors attr then call `.run()`.'
            )

        persian_nums = ('۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹')
        editing_text = ''

        for char in self._editing_text:
            if re.search(r'\d', char):
                editing_text += persian_nums[int(char)]
            else:
                editing_text += char

        self._editing_text = editing_text

    def punctuation_marks_editor(self):
        if self._editing_text is None:
            raise AssertionError(
                'Can\'t access directly to editors, '
                'You must set editors attr then call `.run()`.'
            )

        editing_text = self._editing_text

        # Replace '?' with '‌‌‌‌‌‌‌‌؟'
        while '?' in editing_text:
            editing_text = editing_text.replace('?', '؟')

        # Replace ',' with '،'
        while ',' in editing_text:
            editing_text = editing_text.replace(',', '،')

        # Replace ';' with '؛'
        while ';' in editing_text:
            editing_text = editing_text.replace(';', '؛')

        # Replace '"' with '‌«»'
        quote_mark = '«'

        while '"' in editing_text:
            editing_text = editing_text.replace('"', quote_mark, 1)

            if quote_mark == '»':
                quote_mark = '«'
            else:
                quote_mark = '»'

        self._editing_text = editing_text

    def run(self, original_text):
        self._set_original_text(original_text)
        self._editing_text = self.original_text
        self._general_editor()

        for editor_name in self._editors:
            editor_method = getattr(self, f'{editor_name}_editor')
            editor_method()

        self._edited_text = self._editing_text
        self._editing_text = None

        return self.edited_text

    def set_editors(self, editors):
        if editors is not None:
            if not isinstance(editors, (list, tuple)):
                raise TypeError(
                    "The `editors` option must be a list or tuple. "
                    "Got %s." % type(editors).__name__
                )

            self._editors = []

            for editor_name in editors:
                if not hasattr(self, f'{editor_name}_editor'):
                    raise TypeError(
                        "The `%s` editor doesn't exist in editors list" % editor_name
                    )
                self._editors.append(editor_name)
        else:
            raise AttributeError(
                '`editors` attr can\'t be none.`'
            )

    def _set_original_text(self, text):
        assert text is not None, (
            '`original_text` can\'t be a NoneType object.'
        )

        self.original_text = text

    @property
    def edited_text(self):
        if not hasattr(self, '_edited_text'):
            raise AssertionError(
                'You must call `.run()` before accessing `.edited_text`.'
            )
        return self._edited_text
