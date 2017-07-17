$(document).ready(function() {
	$.ajax({
		type: "GET",
		url: "https://nksv-beta.herokuapp.com/api/users/"+sessionStorage.getItem("u_id")+"/cart",
		headers: {"Content-Type": "application/json", "Authorization": "Token "+sessionStorage.getItem("Token")},
		contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(data,status) {
    	console.log(data);
    	console.log(status);
    	for (var i = 0; i < data.length; i++) {
	    	$("#services-ordered").prepend(`<div class="row">
															            <div class="col-md-1">
															                <p class="cart-elements">`+data[i].id+`</p>
															            </div>
															            <div class="col-md-5">
															                <p id="item-name" class="cart-elements"></p>
															            </div>
															            <div class="col-md-2">
															                <div class="input-sm input-group">
															                  <span class="input-group-addon btn change-qty" role="button">-</span>
															                  <input type="text" class="form-control align-qty" value="1">
															                  <span class="input-group-addon btn change-qty" role="button">+</span>
															                </div>
															            </div>
															            <div id="show-price" class="col-md-2">
																						<p data-price="`+data[i].price+`" id="item-price" class="cart-elements">`+data[i].price+`</p>
															            </div>
															            <div class="col-md-2 adjust-remove-item text-center">
															                <button id="remove-item" class="btn btn-default btn-sm">Remove</button>
															            </div>
															         </div>`);
    	}
    },
    error: function(data,status) {
    	console.log(data);
    	console.log(status);
    }
	});

	$("#services-ordered").on('click', '.change-qty', function() {
					console.log('clicked');
					var oldVal = parseInt($(this).parent().find(".align-qty").val());
					console.log(oldVal);
					const basePrice = $(this).closest(".row").find("#show-price").children().data("price");
					if($(this).text() == '+') {
						var newVal = parseInt(oldVal + 1);
						console.log(newVal);
						var newPrice = parseInt(basePrice * newVal);
					}
					else {
						if(oldVal > 1) {
							var newVal = parseInt(oldVal - 1);
							console.log(newVal);
							var newPrice = parseInt(basePrice * newVal);
						}
						else {
							newVal = 1;
						}
					}
					$(this).parent().find("input").val(newVal);
					$(this).closest(".row").find("#item-price").text(newPrice);
					$.ajax({
						
					});
				});
});