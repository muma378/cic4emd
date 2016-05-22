$(document).ready(function() {
	
	// add class active when hovering navigation bar
	$(".cic-navbar-item").hover(
		function (){
			$( this ).addClass("active")
		}, function () {
			$( this ).removeClass("active")
		}
	);



	
});
