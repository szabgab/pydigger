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
$( "#search" ).autocomplete({
	source: function( request, response ) {
		//console.log('search');
		$.ajax({
			url: "/search/json?package=" + $("#search").val(),
			success: function( data ) {
				//console.log(data.length);
				response(JSON.parse(data));
			}
        });
	},
	minLength: 2
});

//console.log('hello PyDigger - end')
