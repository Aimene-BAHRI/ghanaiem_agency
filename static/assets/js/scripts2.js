
function scroll_to(clicked_link, nav_height) {
	var element_class = clicked_link.attr('href').replace('#', '.');
	var scroll_to = 0;
	if(element_class != '.top-content') {
		element_class += '-container';
		scroll_to = $(element_class).offset().top - nav_height;
	}
	if($(window).scrollTop() != scroll_to) {
		$('html, body').stop().animate({scrollTop: scroll_to}, 1000);
	}
}


jQuery(document).ready(function() {
	
	/*
	    Navigation
	*/
	$('a.scroll-link').on('click', function(e) {
		e.preventDefault();
		scroll_to($(this), $('nav').outerHeight());
	});
	
    /*
        Background
    */
    $('.section-4-container').backstretch("assets/img/backgrounds/bg.jpg");
    
    /*
	    Wow
	*/
	new WOW().init();
	
	/*
	    Carousel
	*/
	$('#carousel-example').on('slide.bs.carousel', function (e) {

	    /*
	        CC 2.0 License Iatek LLC 2018
	        Attribution required
	    */
	    var $e = $(e.relatedTarget);
	    var idx = $e.index();
	    var itemsPerSlide = 4;
	    var totalItems = $('.caroussel1').length;
	    if (idx >= totalItems-(itemsPerSlide-1)) {
	        var it = itemsPerSlide - (totalItems - idx);
	        for (var i=0; i<it; i++) {
	            // append slides to end
	            if (e.direction=="left") {
	                $('.caroussel1').eq(i).appendTo('.carousel-inner1');
	            }
	            else {
	                $('.caroussel1').eq(0).appendTo('.carousel-inner1');
	            }
	        }
	    }
	});
	
	// Carousel 2
	$('#carousel-example2').on('slide.bs.carousel', function (e2) {

	    /*
	        CC 2.0 License Iatek LLC 2018
	        Attribution required
	    */
	    var $e2 = $(e2.relatedTarget);
	    var idx2 = $e2.index();
	    var itemsPerSlide2 = 4;
	    var totalItems2 = $('.caroussel2').length;
	    
	    if (idx2 >= totalItems2-(itemsPerSlide2-1)) {
	        var it2 = itemsPerSlide2 - (totalItems2 - idx2);
	        for (var i=0; i<it2; i++) {
	            // append slides to end
	            if (e2.direction=="left") {
	                $('.caroussel2').eq(i).appendTo('.carousel-inner2');
	            }
	            else {
	                $('.caroussel2').eq(0).appendTo('.carousel-inner2');
	            }
	        }
	    }
	});
	
});
