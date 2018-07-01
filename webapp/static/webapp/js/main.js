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
const apiBaseUrl = 'webapp/v1/';
const newPageUrl = domain + apiBaseUrl + 'data/create/';

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

(function () {
    'use strict';

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

        let data = new FormData();
        let image = $('#image')[0].files;

        if (image.length > 0) {
            data.append('image', image[0]);
        }

        data.append('title', $('#title').val());
        data.append('subtitle', $('#subtitle').val());
        data.append('ann_date', $('#anniversaryDate').val());
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
                myStack.text = 'اطلاعات با موفقیت ارسال شد.';
                myStack.type = 'success';

                PNotify.removeAll();

                new PNotify(myStack);

                $('#newPageModal').modal('toggle');
            },
            error: function (error) {
                myStack.text = error.message;
                myStack.type = 'error';

                PNotify.removeAll();

                new PNotify(myStack);
            }
        })
    });
})();
