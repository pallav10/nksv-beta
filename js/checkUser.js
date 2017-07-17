$(document).ready(function() {

	if(localStorage.key.length > 0 && sessionStorage.getItem("First Name") !== null) {
		var username = sessionStorage.getItem('First Name');
		$(".buttons").html(`<a href="cart.html"><img src="images/cart.png" alt="logo missing" class="brand_name" style="float: right;width: 57px;margin-top: -17px;"></a><button id="logoutButton" class="btn btn-primary btn-sm button1">Logout</button><a href="user_profile.html" class="btn btn-primary btn-sm button2" role="button">Hi, `+username+`</a>`);

		$(".buttons").on('click', 'button', function() {
			sessionStorage.clear();
			window.location.replace("index.html");
		});
	}
});