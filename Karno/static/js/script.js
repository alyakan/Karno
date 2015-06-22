$(document).ready(function(){
	var width = $(window).width();

	/* MASONRY GALLERY */
	var $container = $('.container-gallery');
	$container.imagesLoaded( function(){
    	$container.masonry();
	});

	/* MASONRY PORTFOLIO */
	var $wrapper = $('.wrapper-portfolio');
	$container.imagesLoaded(function(){
		$wrapper.masonry();
	});

	/* TOOLTIP */
	$('[rel="tooltip"]').tooltip();

	/* COLORBOX PORTFOLIO */
	if(width > 767){
		$('.img-group-gallery').colorbox({rel:'gallery-images', width:'auto', height: '90%', current : '{current}/{total}'});
		$('.img-slideshow').colorbox({rel:'gallery-slideshow', width:'auto', height: '90%', slideshow:true, current : '{current}/{total}'});
	}else{
		$('.img-group-gallery').colorbox({rel:'gallery-images', width:'90%', height: 'auto', current : '{current}/{total}'});
		$('.img-slideshow').colorbox({rel:'gallery-slideshow', width:'auto', height: '90%', slideshow:true, current : '{current}/{total}'});
	}
	
	/* SEARCH BOX */
	var searchBox = $('#searchbox');
	$('.btn-search').on('click', function(){
		$(this).toggleClass('active');
		$('.fsearch').toggleClass('active');
		searchBox.toggleClass('searchbox-show');
	});

	if(width > 767){
		/* Hide Search Box on Mouseleave */
		$("#searchbox").mouseleave(function(){
	    	$(".btn-search").toggleClass('active');
			$('.fsearch').toggleClass('active');
	   		searchBox.toggleClass('searchbox-show');
		});
	}

	/* ISOTOPE PORTFOLIO FILTER */
	var container = $('#portfolio-content');    
	container.isotope({
		animationEngine : 'best-available',
		animationOptions: {
			duration: 200,
			queue: false
		},
		layoutMode: 'fitRows'
	}); 

	$('.nav-filter .nav-pills li a').click(function(){
		$('.nav-filter .nav-pills li a').removeClass('active');
		$(this).addClass('active');
		var selector = $(this).attr('data-filter-value');
		container.isotope({ filter: selector });
		return false;
	});

});