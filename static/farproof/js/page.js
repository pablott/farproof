function pageResize() {
    var page_height = $(".page").height();
    var img_height = $(".page img").height();
    var target_height = (page_height / 2) - (img_height / 2);

    // Output
    var str2 = 'page:' + page_height + ' img:' + img_height;
    $('.debug').html(str2);

    // TODO add method for resizing window only after
    $(".page img").stop().animate({
        top: target_height
    }, 200);

}


// JavaScript method
// http://stackoverflow.com/questions/1682495/jquery-resize-to-aspect-ratio
// http://ericjuden.com/2009/07/jquery-image-resize/
// http://professionalaspnet.com/archive/2012/08/05/Get-The-Real-Dimensions-of-an-Image-Using-jQuery.aspx


//function pageRatio () {
//    
//}
//
//function pageResize () {
//
//    // http://benalman.com/projects/jquery-resize-plugin/
//    // Fire redimension when #view changes, use bind or resize.
//    //var max_width = $(".page").width();
//    
//    
//    
//    
//    // Alternative: check whether img is wider than .page
//
//    //var img_size = $(".page img").width();
//    
//    $(window).resize(function() {
//            var page_size = $(".page").width();
//        
//        $('#debug').append('<div>Handler for .resize() called.</div>');
//    
//        //if (img_size > page_size) {
//            $(".page img").css("width",page_size);
//        //$(".page img").css("height",'auto');
//    //}
//    
//    // Output
//    var str2 =  'page:' + page_size /*+ 'img:' + img_size*/;
//    $('.debug').html(str2);    
//    
//    });
//    
//
//    
//
//    
//    
//    
//    //    if ( toggle1 == 0 ) {
//    //        $(".vertical").animate({
//    //            height: 80,
//    //        }, speed1);
//    //    }
//    //    else {
//    //        $(".vertical").animate({
//    //            height: 20,
//    //        }, speed1);
//    //    }
//    //});
//
//    
//    
//    
//    
//}