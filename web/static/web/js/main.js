let myStack = {
    text: null,
    type: null,
    addclass: 'custom',
    icon: false,
    mouse_reset: false,
    buttons: {
        sticker: false,
        closer: false
    }
};
let csrftoken = Cookies.get('csrftoken');
let domain = window.location.origin + '/';
const apiBaseUrl = 'web/v1/';
const newPageUrl = domain + apiBaseUrl + 'data/create/';
const reportUrl = domain + apiBaseUrl + 'report/create/';

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

(function () {
    'use strict';

    $(window).resize(function () {
        resizeImage();
    });

    $(document).ready(function () {
        resizeImage();
    });

    window.addEventListener('load', function () {
        let forms = document.getElementsByClassName('needs-validation');

        Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);

    $('.modal').on('hidden.bs.modal', function () {
        $(this).find('form')[0].reset();
        $('form').removeClass('needs-validation was-validated');
        $('#image').next('.custom-file-label').html('');

        let submit_page = $('#submitPage');
        submit_page.prop('disabled', false);
        submit_page.html('ارسال');

        let submit_report = $('#submitReport');
        submit_report.prop('disabled', false);
        submit_report.html('ارسال');
    });

    $('#searchForm').submit(function () {
        if ($.trim($('#q').val()) === '') {
            return false;
        }
    });

    $('#image').on('change', function () {
        let fileName = $(this).val().replace(/\\/g, '/').replace(/.*\//, '');
        $(this).next('.custom-file-label').html(fileName);
    });

    $('#newPageModal').submit(function (event) {
        event.stopPropagation();
        event.preventDefault();

        let submit_page = $('#submitPage');
        submit_page.prop('disabled', true);
        submit_page.html('');
        submit_page.append('<span class="position-relative fas-reglage"><i class="fas fa-spinner' +
            ' fa-spin"></i></span>');

        let data = new FormData();
        let image = $('#image')[0].files;

        if (image.length > 0) {
            data.append('image', image[0]);
        }

        data.append('title', $('#title').val());
        data.append('subtitle', $('#subtitle').val());
        data.append('event', $('#event').val());
        data.append('content', $('#content').val());
        data.append('image_caption', $('#imageCaption').val());
        data.append('reference', $('#reference').val());
        data.append('author', $('#author').val());

        $.ajax({
            type: 'POST',
            url: newPageUrl,
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            },
            success: function () {
                myStack.text = 'اطلاعات با موفقیت ارسال شد';
                myStack.type = 'success';

                PNotify.removeAll();

                new PNotify(myStack);

                $('#newPageModal').modal('toggle');
            },
            error: function (error) {
                if (error.status === 500) {
                    myStack.text = 'خطای سمت سرور';
                    myStack.type = 'error';
                } else {
                    myStack.text = error.responseJSON.message;
                    myStack.type = 'error';
                }

                PNotify.removeAll();

                new PNotify(myStack);

                let submit_page = $('#submitPage');
                submit_page.prop('disabled', false);
                submit_page.html('ارسال');
            }
        })
    });

    $('#reportModal').submit(function (event) {
        event.stopPropagation();
        event.preventDefault();

        let submit_report = $('#submitReport');
        submit_report.prop('disabled', true);
        submit_report.html('');
        submit_report.append('<span class="position-relative fas-reglage"><i class="fas fa-spinner' +
            ' fa-spin"></i></span>');

        let data = new FormData();

        data.append('body', $('#body').val());
        data.append('reporter', $('#reporter').val());
        data.append('data', $('#id').val());

        $.ajax({
            type: 'POST',
            url: reportUrl,
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            },
            success: function () {
                myStack.text = 'گزارش با موفقیت ارسال شد';
                myStack.type = 'success';

                PNotify.removeAll();

                new PNotify(myStack);

                $('#reportModal').modal('toggle');
            },
            error: function (error) {
                if (error.status === 500) {
                    myStack.text = 'خطای سمت سرور';
                    myStack.type = 'error';
                } else {
                    myStack.text = error.responseJSON.message;
                    myStack.type = 'error';
                }

                PNotify.removeAll();

                new PNotify(myStack);

                let submit_report = $('#submitReport');
                submit_report.prop('disabled', false);
                submit_report.html('ارسال');
            }
        })
    });
})();

function resizeImage() {
    let image = new Image();
    let frame = $('.thumbnail');

    $('.thumbnail img').each(function () {
        image.src = $(this).attr('src');
        let image_ratio = image.naturalWidth / image.naturalHeight;
        let frame_ratio = frame.width() / frame.height();

        if ((image_ratio > 1.0 && image_ratio > frame_ratio) || (image_ratio <= 1.0 && image_ratio >= frame_ratio)) {
            $(this).css('width', 'auto');
            $(this).css('height', '100%');
        } else if ((image_ratio <= 1.0 && image_ratio < frame_ratio) || (image_ratio > 1.0 && image_ratio <= frame_ratio)) {
            $(this).css('width', '100%');
            $(this).css('height', 'auto');
        }
    });
}
