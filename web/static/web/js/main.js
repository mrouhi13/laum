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
let domain = window.location.origin;
const createPageUrl = domain + '/page/create/';
const createReportUrl = domain + '/report/create/';

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

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
        $('#id_image').next('.custom-file-label').html('');

        let submit_page = $('#submitPage');
        submit_page.prop('disabled', false);
        submit_page.html('ارسال');

        let submit_report = $('#submitReport');
        submit_report.prop('disabled', false);
        submit_report.html('ارسال');
    });

    $('#searchForm').submit(function () {
        if ($.trim($('#id_q').val()) === '') {
            return false;
        }
    });

    $('#id_image').on('change', function () {
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
        let image = $('#id_image')[0].files;

        if (image.length > 0) {
            data.append('image', image[0]);
        }

        data.append('title', $('#id_title').val());
        data.append('subtitle', $('#id_subtitle').val());
        data.append('event', $('#id_event').val());
        data.append('content', $('#id_content').val());
        data.append('image_caption', $('#id_image_caption').val());
        data.append('reference', $('#id_reference').val());
        data.append('author', $('#id_author').val());
        console.log('data: ', data);
        $.ajax({
            type: 'POST',
            url: createPageUrl,
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
                myStack.text = 'اطلاعات با موفقیت ارسال شد.';
                myStack.type = 'success';

                PNotify.removeAll();

                new PNotify(myStack);

                $('#newPageModal').modal('toggle');
            },
            error: function (error) {
                if (error.status === 500) {
                    myStack.text = 'خطایی در سرور رخ داده است.';
                    myStack.type = 'error';
                } else if (error.status === 400) {
                    $.each(error.responseJSON, function (key) {
                        console.log('#' + key + '_tooltip_id');
                        $('#' + key + '_tooltip_id').show()
                    });

                    myStack.text = 'ثبت اطلاعات با خطا مواجه شد.';
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

        data.append('body', $('#id_body').val());
        data.append('reporter', $('#id_reporter').val());
        data.append('page', $('#id_page').val());

        $.ajax({
            type: 'POST',
            url: createReportUrl,
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
                myStack.text = 'گزارش با موفقیت ارسال شد.';
                myStack.type = 'success';

                PNotify.removeAll();

                new PNotify(myStack);

                $('#reportModal').modal('toggle');
            },
            error: function (error) {
                if (error.status === 500) {
                    myStack.text = 'خطایی در سرور رخ داده است.';
                    myStack.type = 'error';
                } else if (error.status === 404) {
                    myStack.text = 'صفحه‌ی مورد نظر پیدا نشد.';
                    myStack.type = 'error';
                } else if (error.status === 400) {
                    $.each(error.responseJSON, function (key) {
                        console.log('#' + key + '_tooltip_id');
                        $('#' + key + '_tooltip_id').show()
                    });

                    myStack.text = 'ثبت گزارش با خطا مواجه شد.';
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


