$(document).ready(function() {
	$("#send-reset-request").submit(function(e) {
		e.preventDefault();
		$.ajax({
			type: "POST",
			url: "https://nksv-beta.herokuapp.com/api/password_reset/",
			data: JSON.stringify({"email": $("#reset-email").val()}),
	    contentType: "application/json; charset=utf-8",
	    dataType: "json",
	    success: function(data,status) {
	    	console.log(data);
	    	console.log(status);
	    },
	    error: function(data,status) {
	    	console.log(data);
	    	console.log(status);
	    }
		});
		var fewSeconds = 5;
		$('#send-reset-link').click(function(){
		    var btn = $(this);
		    btn.prop('disabled', true);
		    setTimeout(function(){
		        btn.prop('disabled', false);
		    }, fewSeconds*120);
		});
	});
});