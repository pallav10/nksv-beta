$(document).ready(function() {
	$.ajax({
		type: "GET",
		url: "https://nksv-beta.herokuapp.com/api/categories/"+sessionStorage.getItem("c_id")+"/",
		contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(data,status) {
    	console.log(data);
    	console.log(status);
    	for (var i = 0; i < data.length; i++) {
			$("#load-categories").append("<li><a href='#' style='display: block;' class='productMenu' data-id="+data[i].id+">"+data[i].name+"</a></li>");
			$("#load-categories li:first").addClass("active");
			}
			var x = $("#load-categories li:first a").data("id");
			console.log(x);
			$.ajax({
			type: "GET",
			url: "https://nksv-beta.herokuapp.com/api/categories/"+x+"/items/",
			success: function(data, status) {
				console.log(data);
				for(i=0;i<data.length;i++) {
					$("#load-details").append(`<div>
																			 <h3>`+data[i].name+`</h3>
																			 <div class='row'>
																			 	<div class='col-md-6 col-xs-12'>
																			 		<img src=`+data[i].image+`>
																			 	</div>
																			 	<div class='col-md-6 col-xs-12'>
																			 		<p>`+data[i].description+`</p>
																			 		<div class="row">
																			 			<div class="col-md-4"><p data-price="`+data[i].price+`" class="item-price">INR `+data[i].price+`/- </p></div>
																					 	<div class="col-md-4"><button data-price="`+data[i].price+`" id="buy-item" data-id="`+data[i].id+`" class="btn btn-default buy-items">Add to Cart</button></div>	
																					 	<div class="col-md-4"><a href="cart.html" class="btn btn-default buy-items" role="button">Buy Now</a></div>	
																			 		</div>
																			 	</div>
																			 </div>
																		 </div>`);
				}
			},
			error: function(data, status) {
				console.log(data);
			}
			});
    },
    error: function(data,status) {
    	console.log(data);
    	console.log(status);
    }
	});

	$("#load-categories").on('click', 'li', function(e) {
		e.preventDefault();
		$(this).addClass('active').siblings().removeClass('active');
		var cid = $(e.target).data("id");
		console.log(cid);
		$.ajax({
			type: "GET",
			url: "https://nksv-beta.herokuapp.com/api/categories/"+cid+"/items",
			success: function(data, status) {
				console.log(data);
				console.log(status);
				$("#load-details").empty();
				for(i=0;i<data.length;i++) {
					$("#load-details").append(`<div>
																		   <h3>`+data[i].name+`</h3>
																		   <div class='row'>
																		     <div class='col-md-6 col-xs-12'>
																		     	<img src=`+data[i].image+`>
																		     </div>
																		     <div class='col-md-6 col-xs-12'>
																		     	<p>`+data[i].description+`</p>
																		     	<div class="row">
																			 			<div class="col-md-4"><p class="item-price">INR `+data[i].price+`/- </p></div>
																					 	<div class="col-md-4"><button data-price="`+data[i].price+`" id="buy-item" data-id="`+data[i].id+`" class="btn btn-default buy-items">Add to Cart</button></div>	
																					 	<div class="col-md-4"><a href="cart.html" class="btn btn-default buy-items" role="button">Buy Now</a></div>	
																			 		</div>
																		     </div>
																		   </div>
																		 </div>`);
				}
			},
			error: function(data, status) {
				console.log(data);
			}
		});
	});

	$("#load-details").on("click", "#buy-item", function() {
		var pid = $(this).data("id");
		console.log(pid);
		var price = $(this).data("price");
		console.log(price);
		$.ajax({
			type: "POST",
			url: "https://nksv-beta.herokuapp.com/api/users/"+sessionStorage.getItem("u_id")+"/cart/"+pid+"/",
			headers: {"Content-Type": "application/json", "Authorization": "Token "+sessionStorage.getItem("Token")},
			data: JSON.stringify({"price": price}),
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
	});
});