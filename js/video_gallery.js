$(document).ready(function() {
	$.ajax({
		type: "GET",
		url: "https://nksv-beta.herokuapp.com/api/videos/",
		success: function(data,status) {
			console.log(data);
			console.log(status);
			for (var i = 0; i < data.length; i++) {
				$("#listOfVideos").append(`<div class="col-lg-4 col-md-4 col-sm-6 col-xs-12"><video controls style="width: 360px;" src="`+data[i].video+`"></video></div>`);
			}
		},
		error: function(data,status) {
			console.log(data);
			console.log(status);
		}
	});
});