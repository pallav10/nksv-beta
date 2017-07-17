$(document).ready(function() {
	$("form").submit(function(e) {
		e.preventDefault();
		$.ajax({
	    type: "POST",
	    url: "https://nksv-beta.herokuapp.com/api/password_reset/",
	    data: JSON.stringify({"email": $("#userResetEmail").val()}),
	    contentType: "application/json; charset=utf-8",
	    dataType: "json",
	    success: function(data,status) {
	        console.log(data);
	        console.log(status);
	        console.log("Email sent!");
	    },
	    error: function(data,status){
	        console.log(data);
	        console.log(status);  
	    }
		});
	});
});