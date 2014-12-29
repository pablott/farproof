$(document).ready(function () {
    selectList(); // Get clicked div in #list
    toggleList(); // Show/hide list
    toggleIndex(); // Show toggleIndex 
    toggleToolbar(); // Controls toolbar

    // Adjust on load
    // Chrome needs a delay or img won't have been loaded
    setTimeout(function () {
        pageResize();
    }, 20);
    $(window).resize(function () {   // Adjust on window resize
        //$(this).mouseup(function() {
        setTimeout(function () {
            pageResize();
        }, 100);
        //})
    })

    zoomIn();
    navLeft();
    navRight();
    navFullLeft();
    navFullRight();

});  // End of document ready


var page_selected = 0; // Initialize var, used by several FUNC listSelect
var toggle1 = 0; // index
var toggle2 = 0; // list
var speed = 350;
var blur_speed = 2000; // Time to hide list on mouse leave

// FUNC toggleIndex
function toggleIndex() {

    $("#toggle_index").click(function () {

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
        else {
            $("#index_toolbar").stop().animate({
                bottom: 200
            }, speed);
            $("#view").stop().animate({
                bottom: 200
            }, speed, function () {
                // Animation complete: adjust vertical align
                pageResize();
            });
            $('#index').stop().animate({
                height: 'toggle'
            }, speed);
            pageResize();
            $(this).html('d');
            toggle1 = 0;
        }
    });
} // End FUNC toggleIndex

// FUNC selectList
// closes on after select or after clicking outside
function selectList() {
    $("#list div").click(function () {
        //get number of clicked div inside list
        page_selected = $(this).index();

        // Output debug value
        var str = 'sel: ' + page_selected;
        $('.debug').html(str);

        /* Remove class to all inside list, then add class to clicked div
         * This prevents multiple selection.
         */
        $("#list div").removeClass("selected");
        $(this).addClass("selected");
    });
} // End FUNC selectList

// FUNC hideList
function hideList() {
    $("#toggle_list").stop().animate({
        // Scroll #toggle_list to top or otherwise intereferes with top adjustment
        scrollTop: 0,
        height: '20'
    }, speed);
    $("#list").stop().animate({
        top: -page_selected * 20
    }, speed);
    toggle2 = 0;
} // End FUNC hideList

// FUNC toggleList
function toggleList() {
    // http://stackoverflow.com/questions/1403615/use-jquery-to-hide-a-div-when-the-user-clicks-outside-of-it
    //$("body *").not("#toggle_list").click(function() {
    //
    //
    //        hideList();
    //
    //
    //});

    // List hides when clicking anywhere but the list
    // TODO add an 'always pin' option to make this optional
    // http://stackoverflow.com/questions/3709255/add-delay-to-mouseleave-in-jquery
    var hover = 0;
    $("#toggle_list").mouseenter(function () {
        //mouse enter
        //clearTimeout(myTimer);
        hover = 1;
    })
    $("#toggle_list").mouseleave(function () {
        hover = 0
    })

    $(document).click(function () {
        if (hover == 0) {
            hideList();
        }
    })


    $("#toggle_list").click(function () {
        //function hideList() {}
        var list_height = $("#list").height();
        var list_scroll = page_selected * 20;

        if (toggle2 == 0) {
            $(this).stop().animate({
                scrollTop: page_selected * 20,
                height: list_height
            }, speed);
            $("#list").stop().animate({
                top: '0'
            }, speed);

            toggle2 = 1;
        }
        else {
            hideList();
        }
    });
} // End FUNC toggleList
    
    
    
    
    
    
    
    

