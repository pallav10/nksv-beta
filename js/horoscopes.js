$(document).ready(function() {
	$.ajax({
		type: "GET",
		url: "https://nksv-beta.herokuapp.com/api/horoscopes/",
		success: function(data,status) {
			console.log(data);
			console.log(status);
		},
		error: function(data,status) {
			console.log(data);
			console.log(status);
		}
	});
});