(function($) {
   
    $(document).ready(function() {
	$('#search').typeahead({
	  name: 'professors',
	  local: ['tjang', 'altshuler', 'purohit']
	});
    });

})(window.jQuery)
