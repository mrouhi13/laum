$('#searchForm').submit(function () {
    if ($.trim($("#q").val()) === "") {
        return false;
    }
});
