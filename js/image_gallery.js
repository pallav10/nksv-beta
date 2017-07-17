$(document).ready(function() {
	$.ajax({
		type: "GET",
		url: "https://nksv-beta.herokuapp.com/api/images/",
		success: function(data,status) {
			console.log(data);
			for (var i = 0; i < data.length; i++) {
				$("#listOfImages").append(`<div class="col-lg-3 col-md-3 col-sm-6 col-xs-12"><a class="example-image-link" href="`+data[i].image+`" data-lightbox="example-set" data-title="Click the right half of the image to move forward."><img style="width: 240px; height: auto;" class="example-image" src="`+data[i].image+`" alt=""/></a></div>`);
			}
		},
		error: function(data,status) {
			console.log(data);
			console.log(status);
		}
	});
});