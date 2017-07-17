$(document).ready(function() {
	$.ajax({
		type: "GET",
		url: "https://nksv-beta.herokuapp.com/api/articles/",
		success: function(data,status) {
			console.log(data);
			console.log(status);
			for (var i = 0; i < data.length; i++) {
				$("#blogs").append(` <div class="well blog-style">
																      <div class="media">
																        <a class="pull-left" href="#">
																          <img class="media-object" src="`+data[i].image+`">
																        </a>
																        <div class="media-body">
																          <h4 class="media-heading">`+data[i].name+`</h4>
																          <p class="text-right">By Francisco</p>
																          <p>`+data[i].description+`</p>
																        </div>
																      </div>
																    </div>`);
			}
		},
		error: function(data,status) {
			console.log(data);
			console.log(status);
		}
	});
});