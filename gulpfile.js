var gulp = require('gulp');
var uncss = require('gulp-uncss');
var unusedImages = require('gulp-unused-images');
var plumber = require('gulp-plumber');
var imagemin = require('gulp-imagemin');
var elixir = require("laravel-elixir");


//over-ride laravel-elixir configuration
elixir.config.assetsPath = 'src';
elixir.config.publicPath = '';
elixir.config.viewPath = './';
elixir.config.sourcemaps = false;


//source path configuration
var vendors = 'src/vendors/';
var resourcesAssets = 'src/';
var srcCss = resourcesAssets + 'css/';
var srcJs = resourcesAssets + 'js/';

//destination path configuration
var dest = '';
var destFonts = dest + 'fonts/';
var destCss = dest + 'css/';
var destJs = dest + 'js/';
var destVendors = dest + 'vendors/';

/*
 |--------------------------------------------------------------------------
 | Elixir Asset Management
 |--------------------------------------------------------------------------
 |
 | Elixir provides a clean, fluent API for defining some basic Gulp tasks
 | for your Laravel application. By default, we are compiling the Less
 | file for our application, as well as publishing vendor resources.
 |
 */

var paths = {
    'jquery': vendors + 'jquery/dist/',
    'bootstrap': vendors + 'bootstrap/dist/',
    'fontawesome': vendors + 'font-awesome/',
    'select2': vendors + 'select2/',
    'icheck': vendors + 'iCheck/',
    'gmap3': vendors + 'gmap3/dist/',
    'swiper': vendors + 'swiper/',
    'sweetalert2': vendors + 'sweetalert2/dist/',
    'wow' : vendors + 'wow/',
    'revolutionslider': 'revolution-slider/',
    'bootstrap_select2': vendors + 'select2-bootstrap-theme/'
};

elixir(function(mix) {

    // Copy fonts straight to public
    mix.copy(paths.bootstrap + 'fonts', destFonts);

    //bootstrap
    mix.copy(paths.bootstrap + 'js/bootstrap.min.js', destJs);

    //fontawesome
    mix.copy(srcCss + 'font-awesome.min.css', destCss);
    mix.copy(paths.fontawesome + 'fonts', destFonts);

    //jquery
    mix.copy(paths.jquery + 'jquery.min.js', destJs);

    //select2
    mix.copy(paths.select2 + 'dist/css/select2.min.css', destVendors + 'select2/css');
    mix.copy(paths.select2 + 'dist/js/select2.min.js', destVendors + 'select2/js');

    //icheck
    mix.copy(paths.icheck + 'icheck.js', destVendors + 'iCheck/js');
    mix.copy(paths.icheck + 'skins/all.css', destVendors + 'iCheck/css');
    mix.copy(paths.icheck + 'skins/*', destVendors + 'iCheck/css');

    //gmaps
    mix.copy(paths.gmap3 + 'gmap3.min.js', destVendors + 'gmap3/js/');

   //swiper
	mix.copy(paths.swiper + 'dist/css/swiper.min.css', destVendors + 'swiper/css');
        mix.copy(paths.swiper + 'dist/js/swiper.min.js', destVendors + 'swiper/js');

    //sweetalert2

    mix.copy(paths.sweetalert2 + 'sweetalert2.min.js', destVendors + 'sweetalert2/js/');

    //revolution slider
    mix.copy(paths.revolutionslider + 'rs-plugin/css/settings.css', destVendors + 'revolution-slider/css');
    mix.copy(paths.revolutionslider + 'css/layers.css', destVendors + 'revolution-slider/css');
    mix.copy(paths.revolutionslider + 'css/navigation.css', destVendors + 'revolution-slider/css');
    mix.copy(paths.revolutionslider + 'rs-plugin/js/jquery.themepunch.revolution.min.js', destVendors + 'revolution-slider/js');
    mix.copy(paths.revolutionslider + 'rs-plugin/js/jquery.themepunch.tools.min.js', destVendors + 'revolution-slider/js');
    mix.copy(paths.revolutionslider + 'rs-plugin/assets/', destVendors + 'revolution-slider/assets');
    mix.copy(paths.revolutionslider + 'rs-plugin/font/', destVendors + 'revolution-slider/font');


    //wow
    mix.copy(paths.wow + 'css/libs/animate.css', destVendors + 'wow/css');
    mix.copy(paths.wow + 'dist/wow.min.js', destVendors + 'wow/js');

    //bootstrap select2
    mix.copy(paths.bootstrap_select2 + 'dist/select2-bootstrap.min.css', destVendors + 'bootstrap_select2/css');

    /*
    browserSync for auto-reloading browser on changes
     */
    mix.browserSync({
        files: ['**/*.html', '**/*.css', '**/*.js'],
        proxy: undefined,
        server: {
            baseDir: "./"
        }
    });

    mix.sass('bootstrap.scss','css/bootstrap.css');
    mix.sass('sweetalert2.scss','css/sweetalert2.css')
    mix.sass('custom.scss','css/custom.css');
    mix.copy(srcJs + 'custom.js', destJs);
});


/*
| Finds un-used css and outputs css files into out folder
| NOTE: sometimes even for used classes, it shows false positibe, be careful
 */
//directory
gulp.task('uncss', function () {
    //medical
    return gulp.src([
        // include custom css files here
    ])
        .pipe(uncss({
            html: ['**/*.html']
        }))
        .pipe(gulp.dest('./out'));

});

/*
| Find for un-used images and show log
*/
gulp.task('images:filter', function () {
    return gulp.src(['images/**/*'])
        .pipe(plumber())
        .pipe(unusedImages({log:true, delete:false}))
        .pipe(plumber.stop());
});


/*
 | image minimisation
 */
gulp.task('images:min', function(){
    return gulp.src('images/**/*.+(png|jpg|gif|svg)')
        .pipe(imagemin())
        .pipe(gulp.dest('images/'))
});
