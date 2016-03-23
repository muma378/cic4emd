/* 
 * add csrf_tokes for ajax request
 */

(function($){
	'use strict';
	$(document).ready(function(){
		var csrftoken = getCookie('csrftoken');
	
		$(document).on( "click", "a.cke_dialog_tab[id*='cke_Upload_']", function(e){
			var targetForm = $("iframe.cke_dialog_ui_input_file").contents().find("form")
			if (targetForm.children('input[name="csrfmiddlewaretoken"]').length == 0){
				var csrf_label = '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '">';
				targetForm.prepend(csrf_label);
				// replace the default name with attribute name of model Figure
				targetForm.children('input[name="upload"]').attr('name', 'image');
			}
		})
		
			
	});
})(django.jQuery);

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = django.jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

