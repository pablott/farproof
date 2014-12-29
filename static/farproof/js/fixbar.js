//http://stackoverflow.com/questions/6980821/fix-object-to-top-of-browser-window-when-scrolling
//http://jsfiddle.net/cc48t/

document.ready = function () {
    $('#view').scroll(function () {

        // Add shadow to .list_header when scrolled
        if ($('#view').scrollTop() > 0) {
            $('.list_header').addClass("scrolled");
        }
        else {
            $('.list_header').removeClass("scrolled");
        }

        // Output debug values:
        var scrollX = $('#view').scrollLeft();
        var scrollY = $('#view').scrollTop();
        var pos = scrollX + ', ' + scrollY;
        $('.debug').html(pos);

        // Set 'top' position of .list_header to wherever scroll is
        // only if #view has been vertically OR horizontally scrolled
        // ('left' is presumed 0)
        if ($('#view').scrollTop() > 0 || $('#view').scrollLeft() > 0) {
            $('.list_header').css({
                'top': $('#view').scrollTop(),
                'right': -$('#view').scrollLeft()
            });
        }
        // Or else it means #view is not scrolled;
        // it has to be reset because the previous condition
        // never gets down to zero again.
        else {
            $('.list_header').css('top', '0');
        }
    });
};
