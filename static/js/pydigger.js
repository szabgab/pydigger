//console.log('hello PyDigger - start')
$("#jump_to").attr('disabled', 'disabled');
$("#diff_with").attr('disabled', 'disabled');

$("#version_selector").on('change', function( event ) {
	//console.log($(this).val());
	if ( $(this).val() == "") {
		$("#jump_to").attr('disabled', 'disabled');
		$("#diff_with").attr('disabled', 'disabled');
	} else {
		$("#jump_to").removeAttr('disabled');
		$("#diff_with").removeAttr('disabled');
	}
//	$(this).parent().submit()
});

$("#jump_to").on('click', function( event ) {
	var url = '/package/' + $("#package_name").val() + '/' + $("#version_selector").val();
	console.log('jump to ' + url);
	window.location = url;
	//$(this).parent().submit()
});
$("#diff_with").on('click', function( event ) {
	//console.log('diff');
	alert('not implemented yet');
	//var url = '/diff?source=
});

var availableTags = [];
//$( "#search_form" ).on('submit', function( event ) {
//	console.log('search: ' + $("#search").val());
//	event.preventDefault();
//});

$( "#search" ).autocomplete({
	source: function( request, response ) {
		//console.log('search');
		$.ajax({
			url: "/search/json?package=" + $("#search").val(),
			success: function( data ) {
				//console.log(data.length);
				// In order to allow the user to search for arbitrary string as well we add the current string as the first
				// option
				var list = JSON.parse(data);
				var val =$("#search").val();
				if (list.indexOf(val) == -1) {
					list.splice(0, 0, val);
				}
				response(list);
			}
        });
	},
	minLength: 2,
	select: function( event, ui ) {
		console.log('hi');
        console.log( ui.item ?
          "Selected: " + ui.item.label :
          "Nothing selected, input was " + this.value);
		$( "#search_form" ).submit();
      },
      open: function() {
		//console.log('open');
		// fires when the selection list is shown
        //$( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
      },
      close: function() {
		//console.log('close');
		// fires when the selection list is close (by pressing ESC)
        //$( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
      }
});

//console.log('hello PyDigger - end')
