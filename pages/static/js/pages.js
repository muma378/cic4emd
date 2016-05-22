$(document).ready(function() {
	
	var activate = function (elem) {
		elem.hover(
				function (){
				$(this).siblings(".active").removeClass("active")
				$( this ).addClass("active")
			}, function () {
				$( this ).removeClass("active")
			}
		)
	};

	// add class active when hovering navigation bar
	activate($(".cic-navbar-item"));
	// add class active when hovering news 
	// activate($(".cic-trend-item"));
	$(".cic-trend-item").hover(
				function (){
				$(this).siblings(".active").removeClass("active")
				$( this ).addClass("active")
			}, function () {}
		)

	
});
