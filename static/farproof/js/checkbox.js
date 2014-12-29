// http://briancray.com/posts/check-all-jquery-javascript

$(function () {
    $('.checkall').click(function () {
        $('.list_container:eq(0)').find(':checkbox').prop('checked', this.checked);
        alert(page_set);
    });

    $('.list_container :checkbox').click(function () {
        var checked = 0;
        var total_pages = 0;
        for $('.list_container') in (.find(':checked')) {
            checked = checked + 1;
            total_pages = total_pages + 1;
        }
        ;

        if checked = total_pages {
            alert('sdasd');
            $('.checkall').class('debug');

        }
    });

});
    