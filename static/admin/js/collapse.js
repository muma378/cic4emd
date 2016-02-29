/*global gettext*/
(function($) {
    'use strict';
    $(document).ready(function() {
        // Add anchor tag for Show/Hide link
        $("fieldset.collapse").each(function(i, elem) {
            // Don't hide if fields in this fieldset have errors
            if ($(elem).find("div.errors").length === 0) {
            	
                $(elem).addClass("collapsed").find("h2").wrap('<a id="fieldsetcollapser' +
                    i + '" class="collapse-toggle" style="text-decoration:none;" href="#"></a>');
            }
        });
        // Add toggle to anchor tag
        $("fieldset.collapse a.collapse-toggle").click(function(ev) {
            if ($(this).closest("fieldset").hasClass("collapsed")) {
                // Show
                $(this).closest("fieldset").removeClass("collapsed").trigger("show.fieldset", [$(this).attr("id")]);
            } else {
                // Hide
                $(this).closest("fieldset").addClass("collapsed").trigger("hide.fieldset", [$(this).attr("id")]);
            }
            return false;
        });
    });
})(django.jQuery);
