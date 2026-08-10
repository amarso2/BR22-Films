// some scripts

// jquery ready start
$(document).ready(function() {
	// jQuery code


    /* ///////////////////////////////////////

    THESE FOLLOWING SCRIPTS ONLY FOR BASIC USAGE, 
    For sliders, interactions and other

    */ ///////////////////////////////////////
    

	//////////////////////// Prevent closing from click inside dropdown
    $(document).on('click', '.dropdown-menu', function (e) {
      e.stopPropagation();
    });


    $('.js-check :radio').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $('input[name='+ check_attr_name +']').closest('.js-check').removeClass('active');
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');

        } else {
            item.removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });


    $('.js-check :checkbox').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');
        } else {
            $(this).closest('.js-check').removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });



	//////////////////////// Bootstrap tooltip
	if($('[data-toggle="tooltip"]').length>0) {  // check if element exists
		$('[data-toggle="tooltip"]').tooltip()
	} // end if




    
}); 

// Highlight navbar links when their sections are in view
$(function(){
    var navLinks = document.querySelectorAll('.navbar-nav .nav-link[href^="#"]');
    var sections = [];
    navLinks.forEach(function(link){
        var id = link.getAttribute('href');
        if(id && id.startsWith('#')){
            var sec = document.querySelector(id);
            if(sec) sections.push(sec);
        }
    });

    if('IntersectionObserver' in window && sections.length){
        var opts = { root: null, rootMargin: '0px 0px -40% 0px', threshold: 0 };
        var obs = new IntersectionObserver(function(entries){
            entries.forEach(function(entry){
                if(entry.isIntersecting){
                    var id = '#' + entry.target.id;
                    navLinks.forEach(function(link){
                        if(link.getAttribute('href') === id){
                            link.classList.add('active');
                        } else {
                            link.classList.remove('active');
                        }
                    });
                }
            });
        }, opts);
        sections.forEach(function(s){ obs.observe(s); });
    } else {
        // Fallback: on scroll compute nearest section
        var $win = $(window);
        function updateActive(){
            var fromTop = $win.scrollTop() + 80;
            var current = null;
            sections.forEach(function(s){ if(s.offsetTop <= fromTop) current = s; });
            if(current){
                var id = '#' + current.id;
                navLinks.forEach(function(link){
                    if(link.getAttribute('href') === id) link.classList.add('active'); else link.classList.remove('active');
                });
            }
        }
        $win.on('scroll', updateActive);
        updateActive();
    }
});
// jquery end

