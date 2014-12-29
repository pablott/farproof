// FUNC toggleToolbar
<<<<<<< HEAD
function toggleToolbar() {

=======
function toggleToolbar () {
    
>>>>>>> 17b09ee... INITIAL COMMIT!!
    var speed1 = 180; // Slide animation
    var speed2 = 500; // Opacity change
    var toggle1 = 0;
    var toggle2 = 0;
<<<<<<< HEAD

=======
    
>>>>>>> 17b09ee... INITIAL COMMIT!!
    // Fade function
    // http://api.jquery.com/mouseleave/
    // This animation is out of the queue because it conflicts with the other animation
    //$(".btn_black").mouseenter(function () {
    //    $(this).animate({
    //            color: "#a7bf51",
    //    },  {duration: speed2, queue: false})      
    //    .mouseleave(function(){
    //        $(this).animate({
    //             color: "#ffffff",
    //        },  {duration: speed2, queue: false});
    //    })
    //});

<<<<<<< HEAD

    $(".vertical div:first-child").click(function () {
        if (toggle1 == 0) {
            $(".vertical").animate({
                height: 80
=======
    
    
    $(".vertical div:first-child").click(function () {
        if ( toggle1 == 0 ) {
            $(".vertical").animate({
                height: 80,
>>>>>>> 17b09ee... INITIAL COMMIT!!
            }, speed1);
            //$(this).html('u');
            toggle1 = 1;
        }
        else {
            $(".vertical").animate({
<<<<<<< HEAD
                height: 20
=======
                height: 20,
>>>>>>> 17b09ee... INITIAL COMMIT!!
            }, speed1);
            //$(this).html('d');
            toggle1 = 0;
        }
    });
<<<<<<< HEAD

    $(".horizontal div:first-child").click(function () {
        if (toggle2 == 0) {
            $(".horizontal").animate({
                width: 200
=======
    
    $(".horizontal div:first-child").click(function () {
        if ( toggle2 == 0 ) {
            $(".horizontal").animate({
                width: 200,
>>>>>>> 17b09ee... INITIAL COMMIT!!
            }, speed1);
            toggle2 = 1;
        }
        else {
            $(".horizontal").animate({
<<<<<<< HEAD
                width: 80
            }, speed1);
            toggle2 = 0;
        }
    });
=======
                width: 80,
            }, speed1);
            toggle2 = 0;
        }
    });    
>>>>>>> 17b09ee... INITIAL COMMIT!!
}