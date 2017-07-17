$(document).ready(function() {
	$("#edit-personal-details").submit(function(e) {
		e.preventDefault();
		console.log(sessionStorage.getItem("Token"));
		$.ajax({
			type: "PUT",
			url: "https://nksv-beta.herokuapp.com/api/users/"+sessionStorage.getItem("u_id")+"/",
			headers: {"Content-Type": "application/json", "Authorization": "Token "+sessionStorage.getItem("Token")},
			data: JSON.stringify({"first_name": $("#edit-first-name").val(),"last_name": $("#edit-last-name").val(),"email": $("#edit-user-email").val(),"contact_no": $("#edit-user-contact").val(),"city": $("#edit-city-name").val()}),
	    contentType: "application/json; charset=utf-8",
	    dataType: "json",
	    success: function(data,status) {
	    	console.log(data);
	    	console.log(status);
	    	$("#edit-details").append("<p>Your changes have been successfully saved</p>");
	    },
	    error: function(data,status) {
	    	console.log(data);
	    	console.log(status);
	    }
		});
	});
	$("#update-password").submit(function(e) {
		e.preventDefault();
		$.ajax({
			type: "PUT",
			url: "https://nksv-beta.herokuapp.com/api/users/"+sessionStorage.getItem("u_id")+"/change_password/",
			headers: {"Content-Type": "application/json", "Authorization": "Token "+sessionStorage.getItem("Token")},
			data: JSON.stringify(),
	    contentType: "application/json; charset=utf-8",
	    dataType: "json",
	    success: function(data,status) {
	    	console.log(data);
	    	console.log(status);
	    	$("#edit-password").append("<p>Your password has been updated</p>");
	    },
	    error: function(data,status) {
	    	console.log(data);
	    	console.log(status);
	    }
		});
	});
});