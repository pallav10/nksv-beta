$(document).ready(function () {
		$("#guest-cart").css("cursor", "default");
    $('#guest-cart').on("click", function(e) {
        e.preventDefault();
        $("#guest-cart-message").text("Please login to view cart");
    });
});