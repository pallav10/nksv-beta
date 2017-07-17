'use strict';
/*
 Theme Name:  - Astrology Bootstrap HTML template
 Author: Jyostna
 Author URI: http://themeforest.net/user/jyostna
 Version: 1.0

 -------------------------------------------- */
/*
 TABLE OF CONTENT
 -------------------------------------------------
 1- Preloader Section
 2- Back-to-top Section
 3- Select2
 4- Icheck
 5- Elements Page
 6- Home Page
 7- Love_Compatibility_Result Page
 8- Love_Compatibility Page
 9- Signs Page
 10- Sign_Single Page
 11- Footer Section
 12- Contact_Us Page
 13- Games Page
 14- Header
 15- Gemstones Single Page
 ---------------------------------------------------
 */

/*=================== Preloader Section ===================*/
var windowWidth = $(window).width();
$(window).on('load',function() {
    $('.preloader').fadeOut();
    return false;
});
/*======================================*/
/*=================== Back-to-top Section ===================*/
var back_top = $('.back-to-top');
$(window).on('scroll',function(){
    if ($(this).scrollTop() >=50) {
        back_top.fadeIn(200);
    } else {
        back_top.fadeOut(200);
    }
});
$(document).on('ready',function() {


    back_top.on('click', function () {
        $('html, body').animate({scrollTop: 0}, 1000);
        return false;
    });
    /*======================================*/
    /*=================== Select2 ===================*/

    if ($.fn.select2 !== undefined) {
        $('.select1, .select2, .home_select').select2({
            theme: 'bootstrap',
            placeholder: "Select here"

        });

        $(".footer_select").select2({
            theme: 'bootstrap',
            placeholder: "Select Month"

        });
        $(".footer_select2").select2({
            theme: 'bootstrap',
            placeholder: "Select Date"

        });

        $('.home_select').select2({
            theme: 'bootstrap',
            placeholder: "Month"

        });
        $('.home_select1').select2({
            theme: 'bootstrap',
            placeholder: "Date"

        });
        $('.home_select2').select2({
            theme: 'bootstrap',
            placeholder: "Year"

        });

        $(".love_select").select2({
            theme: 'bootstrap',
            placeholder: "select your sign"
        });
        $(".footer_select3").select2({
            theme: 'bootstrap',
            placeholder: "0"
        });
        $(".contact_select").select2({
            theme: 'bootstrap',
            placeholder: "Customer service"

        });
    }

    /*======================================*/

    /*=================== Icheck ===================*/

    if ($.fn.iCheck !== undefined) {
        $('input[type="checkbox"], .radio1, .radio2').iCheck({
            checkboxClass: 'icheckbox_minimal-pink',
            radioClass: 'iradio_flat-grey'
        });

    }
    /*======================================*/

    /*=================== Elements Page ===================*/
    var panel_col = $(".panel-collapse");
    panel_col.on('shown.bs.collapse', function () {
        $(this).parent(".panel").find(".accord_desc > .fa-stack > .fa-stack-1x").removeClass("fa-angle-down").addClass("fa-angle-up");
    });
    panel_col.on('hide.bs.collapse', function () {
        $(this).parent(".panel").find(".accord_desc > .fa-stack > .fa-stack-1x").removeClass("fa-angle-up").addClass("fa-angle-down");
    });

    $('.btn_align').on('mouseenter mouseleave', function () {
        $(this).find('.btn_icon').toggleClass('text-primary');
        return false;
    });

    /*======================================*/

    /*=================== Home Page ===================*/
    if (windowWidth > 1200) {
        $(".home_pic1").on('mouseenter mouseleave', function () {
            $(this).closest(".col-md-4").find('.blog_text').toggleClass("displaytext");
        });

        $(".blog_text").on('mouseenter mouseleave', function () {
            $(this).toggleClass("displaytext");
            return false;
        });

    }
    $('.main').on('mouseenter mouseleave', function () {
        $(this).parent().find('.rotate').toggleClass('over');
        return false;
    });

    new WOW().init();
    /*======================================*/

    /*=================== Love_Compatibility_Result Page ===================*/

    var swiper10 = new Swiper('.love-swiper', {
        nextButton: '.next-arrow',
        prevButton: '.previous-arrow',
        loop: true
    });
    $('.color-info, .previous-arrow, .next-arrow, .insight-color').on('mouseenter', function () {
        $(this).css('color', '#e36480');
    });
    $('.color-info, .previous-arrow,.next-arrow').on('mouseleave', function () {
        $(this).css('color', '#4b3065');
    });
    $('.insight-color').on('mouseleave', function () {
        $(this).css('color', '#494949');
    });
    /*======================================*/

    /*=================== Love_Compatibility Page ===================*/

    $('#zodaic_sign').on('change', function () {
        $('.sign').hide();
        $('.' + $(this).val()).show();
    });
    $('#zodaic_sign1').on('change', function () {
        $('.sign1').hide();
        $('.' + $(this).val()).show();
    });
    /*======================================*/

    /*=================== Signs Page ===================*/

    if (windowWidth < 350) {
        $(".sign_btnpadding").addClass("font11");
    }
    /*======================================*/

    /*=================== Sign_Single Page ===================*/

    var swiper1 = new Swiper('.single_swiper', {
        pagination: '.swiper-pagination',
        paginationClickable: true,
        autoplay: 2000,
        loop: true,
        slidesPerView: 5,
        spaceBetween: 20,
        nextButton: '.single_swiper_next',
        prevButton: '.single_swiper_prev',
        breakpoints: {
            340: {
                slidesPerView: 2,
                spaceBetween: 15
            },
            490: {
                slidesPerView: 3,
                spaceBetween: 5
            },
            690: {
                slidesPerView: 4
            },
            760: {
                slidesPerView: 5
            }
        }
    });

    $('.single_arrow').on('click', function () {
        $('.tab_active').click();
    });
    /*======================================*/

    /*=================== Footer Section ===================*/

    $(".go").on('click',function () {
        var month = $(".var1");
        var date = $(".var2");
        var x = month.val();
        var y = date.val();
        $(".go").attr('disabled', true);
        month.attr('disabled', true);
        date.attr('disabled', true);
        for (var i = 0; i < x; i++) {
            var z = Math.floor((Math.random() * y) + 1);
            var footer_sign = $(".pararesult");
            footer_sign.append(z + ", ");
            var m = footer_sign.text();
            var r = m.slice(0, -2);
            var n = r.toString();
            $(".result").val(n);

        }

    });
    $(".clear").on('click', function () {
        var h = $(".pararesult").text("");
        var footer_res = $(".result");
        footer_res.text(h);
        footer_res.val("");
        $(".go").attr('disabled', false);
        $(".var1").attr('disabled', false);
        $(".var2").attr('disabled', false);


    });

    function zodiac(day, month) {
        var zodiac = ['', 'Capricorn', 'Aquarius', 'Pisces', 'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn'];
        var last_day = ['', 19, 18, 20, 20, 21, 21, 22, 22, 21, 22, 21, 20, 19];
        return (day > last_day[month]) ? zodiac[month * 1 + 1] : zodiac[month];
    }
    $(".zodiacname").on('click', function () {
        var day = $(".day").val();
        var month = $(".month").val();
        var z_sign = zodiac(day, month);
        if (z_sign === undefined) {
            swal({
                type: 'error',
                html: 'Please Select Date and Month'
            })
        }
        else {
            swal({
                type: 'success',
                html: 'Hey! Your Zodiac Sign is: <br><h1>' + z_sign + '</h1>'
            });
        }
    });



    function valid_email_address(email) {
        var pattern = new RegExp(/^[+a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i);
        return pattern.test(email);
    }

    $('#subscribe').on('submit',function () {
        if (!valid_email_address($("#email").val())) {
            swal({
                type: 'error',
                html: 'Please Enter Valid Email Address'
            })
        }
        else {
            $.ajax({
                url: 'subscribe.php',
                data: $('#email').serialize(),
                type: 'POST',
                success: function (msg) {
                    swal({
                        type: 'success',
                        html: 'You have Successfully Subscribed'
                    });
                }
            });
        }

        return false;
    });




    /*======================================*/

    /*=================== Contact_Us Page ===================*/

    if ($.fn.gmap3 !== undefined) {
        $("#contact_map").gmap3({
            map: {
                options: {
                    center: [40.3140, -74.5089],
                    zoom: 6,
                    styles: [
                        {
                            "featureType": "road",
                            "stylers": [
                                {
                                    "hue": "#5e00ff"
                                },
                                {
                                    "saturation": -79
                                }
                            ]
                        },
                        {
                            "featureType": "poi",
                            "stylers": [
                                {
                                    "saturation": -78
                                },
                                {
                                    "hue": "#6600ff"
                                },
                                {
                                    "lightness": -47
                                },
                                {
                                    "visibility": "off"
                                }
                            ]
                        },
                        {
                            "featureType": "road.local",
                            "stylers": [
                                {
                                    "lightness": 22
                                }
                            ]
                        },
                        {
                            "featureType": "landscape",
                            "stylers": [
                                {
                                    "hue": "#6600ff"
                                },
                                {
                                    "saturation": -11
                                }
                            ]
                        },
                        {},
                        {},
                        {
                            "featureType": "water",
                            "stylers": [
                                {
                                    "saturation": -65
                                },
                                {
                                    "hue": "#1900ff"
                                },
                                {
                                    "lightness": 8
                                }
                            ]
                        },
                        {
                            "featureType": "road.local",
                            "stylers": [
                                {
                                    "weight": 1.3
                                },
                                {
                                    "lightness": 30
                                }
                            ]
                        },
                        {
                            "featureType": "transit",
                            "stylers": [
                                {
                                    "visibility": "simplified"
                                },
                                {
                                    "hue": "#5e00ff"
                                },
                                {
                                    "saturation": -16
                                }
                            ]
                        },
                        {
                            "featureType": "transit.line",
                            "stylers": [
                                {
                                    "saturation": -72
                                }
                            ]
                        },
                        {}
                    ]
                }
            },
            marker: {
                values: [{
                    address: "Spring Haven Trail,New Jersey",
                    options: {
                        icon: "images/marker1.png"
                    }

                }]
            }

        });
    }
    /*======================================*/

    /*=================== Games Page ===================*/

    var card_dataarr = [
        {card_name: "Wheel Of Fortune"},
        {card_name: "The Chariot"},
        {card_name: "The Magician"},
        {card_name: "The Fool"},
        {card_name: "The Death"},
        {card_name: "Temperance"},
        {card_name: "The World"},
        {card_name: "The Devil"},
        {card_name: "The Star"},
        {card_name: "The Force"},
        {card_name: "The Sun"},
        {card_name: "The Hanged Man"}
    ];

    $('.card_toggle').hide();
    var expanded = 0;
    $(".back").html("<img src='images/1.png'>").hide();
    var imgarr = [];
    var games_img = $(".image_holder");

    games_img.find(".front").hide();
    games_img.find(".flipper:first-child .front").show();
    games_img.find(".flipper .front").on("click", function () {
        if (expanded == 0) {
            $(".image_holder .flipper .front").each(function () {
                if (!$(".flipper").hasClass("flippedimg")) {

                    imgarr.push($(this));

                }
                $('.card_desc').hide();

            });
            expanded = 1;

            showimg();
        }
        else if (!$(".flipper").hasClass("flippedimg")) {
            var num = Math.floor(Math.random() * 11);
            var random_card = num + ".png";
            $(".back").html("<img src='images/" + random_card + "'>");
            $('.image_change').html("<img src='images/" + random_card + "' class='img-responsive'>");
            $(".text_change h3").text(card_dataarr[num].card_name);
            $(this).next(".back").show();
            $(this).hide();
            $(this).closest(".flipper").addClass("flippedimg");
            $('.card_toggle').show();
        }

    });

    function showimg() {
        var card = imgarr.pop();
        card.css('display', "inline-block");
        if (imgarr.length) {
            setTimeout(showimg, 100);
        }
    }


    $(".reset").on("click", function () {
        $('body').find(".flippedimg").removeClass("flippedimg");
        expanded = 0;
        games_img.find(".front,.back").hide();
        games_img.find(".flipper:first-child .front").show();
        $('.card_desc').show();
        $('.card_toggle').hide();
    });

    /*======================================*/

    /*=================== Header Section ===================*/

    $(".info1").on('mouseenter mouseleave', function () {
        $(this).siblings(".header_bg").toggleClass("info2");
        return false;
    });

    function dropdownEffectData(target) {

        var effectInDefault = null,
            effectOutDefault = null;
        var dropdown = $(target),
            dropdownMenu = $('.dropdown-menu', target);
        var parentUl = dropdown.parents('ul.nav');
        if (parentUl.size() > 0) {
            effectInDefault = parentUl.data('dropdown-in') || null;
            effectOutDefault = parentUl.data('dropdown-out') || null;
        }

        return {
            target: target,
            dropdown: dropdown,
            dropdownMenu: dropdownMenu,
            effectIn: dropdownMenu.data('dropdown-in') || effectInDefault,
            effectOut: dropdownMenu.data('dropdown-out') || effectOutDefault
        };
    }

    function dropdownEffectStart(data, effectToStart) {
        if (effectToStart) {
            data.dropdown.addClass('dropdown-animating');
            data.dropdownMenu.addClass('animated');
            data.dropdownMenu.addClass(effectToStart);
        }
    }

    function dropdownEffectEnd(data, callbackFunc) {
        var animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
        data.dropdown.one(animationEnd, function () {
            data.dropdown.removeClass('dropdown-animating');
            data.dropdownMenu.removeClass('animated');
            data.dropdownMenu.removeClass(data.effectIn);
            data.dropdownMenu.removeClass(data.effectOut);

            if (typeof callbackFunc == 'function') {
                callbackFunc();
            }
        });
    }


    if (windowWidth > 768) {
        $(".dropdown-toggle").on('mouseenter', function () {
            $(this).click();
            return false;
        });
        $(".header_li").on('mouseenter', function () {
            $(".dropdown").removeClass("open");
            return false;
        });
        $("header").on('mouseleave', function () {
            $(".dropdown").removeClass("open");
            return false;
        });
        var dropdownSelectors = $('.dropdown, .dropup');


        dropdownSelectors.on({
            "show.bs.dropdown": function () {
                // On show, start in effect
                var dropdown = dropdownEffectData(this);
                dropdownEffectStart(dropdown, dropdown.effectIn);
            },
            "shown.bs.dropdown": function () {
                // On shown, remove in effect once complete
                var dropdown = dropdownEffectData(this);
                if (dropdown.effectIn && dropdown.effectOut) {
                    dropdownEffectEnd(dropdown, function () {
                    });
                }
            },
            "hide.bs.dropdown": function (e) {
                // On hide, start out effect
                var dropdown = dropdownEffectData(this);
                if (dropdown.effectOut) {
                    e.preventDefault();
                    dropdownEffectStart(dropdown, dropdown.effectOut);
                    dropdownEffectEnd(dropdown, function () {
                        dropdown.dropdown.removeClass('open');
                    });
                }
            }
        });
    }


    /*=========Header Section End=========================*/

    /*==========Gemstones single page======================*/
    var swiper11 = new Swiper('.gemstone_swiper', {
        pagination: '.swiper-pagination',
        paginationClickable: true,
        nextButton: '.swiper-button-next',
        prevButton: '.swiper-button-prev',
        slidesPerView: 2,
        autoplay: 2000,
        loop: true,
        breakpoints: {
            450: {
                slidesPerView: 1
            }
        }
    });
});
/*==========Gemstones single page end===========*/

