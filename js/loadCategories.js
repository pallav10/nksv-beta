$(document).ready(function() {
		$.ajax({
			type: "GET",
			url: "https://nksv-beta.herokuapp.com/api/categories/",
			contentType: "application/json; charset=utf-8",
	    dataType: "json",
	    success: function(data,status) {
	    	$("#list-of-categories").empty();
	    	for (var i = 0; i < data.length; i++) {
	    		$("#list-of-categories").append(`<li id="categoryID`+data[i].id+`" data-id="`+data[i].id+`"><a href="shop.html">`+data[i].name+`</a></li>`);
	    	}
	    	$("#list-of-categories").on("click", "li", function() {
					sessionStorage.setItem("c_id", $(this).data("id"));
				});
	    },
	    error: function(data,status) {
	    	console.log(data);
	    	console.log(status);
	    }
		});
});