$(document).ready(function() {
	$.ajax({
		type: "GET",
		url: "https://nksv-beta.herokuapp.com/api/categories/",
		contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(data) {
    	console.log(data);
    	var categories = data.map((value) => value.name);
    	console.log(categories);
    	var sIndex = categories.indexOf("service") + 1;
    	console.log(sIndex);
    	sessionStorage.setItem("sc_id", sIndex);
    },
    error: function(data,status) {
    	console.log(data);
    	console.log(status);
    }
	});

	$.ajax({
		type: "GET",
		url: "https://nksv-beta.herokuapp.com/api/categories/"+sessionStorage.getItem("sc_id")+"/",
		success: function(data,status) {
			console.log(data);
			console.log(status);
			for (var i = 0; i < data.length; i++) {
				$("#load-services").append(`<div class="col-md-4 col-sm-12 col-xs-12 wow fadeInDown" data-wow-duration="1s" data-wow-delay="0.1s">
							                        <div class="col-md-12">
							                            <img id="service-image" src="`+data[i].image+`" alt="image-missing" class="pujaImage img-responsive img-rounded">
							                        </div>
							                        <div class="col-md-12">
							                            <a href="shop.html" class="main">
							                                <div class="sign_card text-center signs_bg">
							                                    <span id="service-name" class="text-aries signs_clr font16">`+data[i].name+`</span><br>
							                                    <span class="signtext_clr font12">₹11000.00</span>
							                                </div>
							                            </a>
							                        </div>
						                        </div>`);
			}
		},
		error: function(data,status) {
			console.log(data);
			console.log(status);
		}
	});

	$(".main").click(function() {
		
	});
});