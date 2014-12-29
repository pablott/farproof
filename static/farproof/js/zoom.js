function zoomIn() {
    $("#zoomIn").click(function () {
        $("#page_container").css


        if (toggle1 == 0) {
            $("#index_toolbar").stop().animate({
                bottom: 0
            }, speed);
            $("#view").stop().animate({
                bottom: 0
            }, speed, function () {
                // Animation complete: adjust vertical align
                pageResize();
            });
            $('#index').stop().animate({
                height: 'toggle'
            }, speed);

            $(this).html('u');
            toggle1 = 1;
        }

    });

}