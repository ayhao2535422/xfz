var gulp = require("gulp");
var cssnano = require("gulp-cssnano");
var rename = require("gulp-rename");
var uglify = require("gulp-uglify");
var cache = require("gulp-cache");
var imagemin = require("gulp-imagemin");
var bs = require("browser-sync").create();
var sass = require("gulp-sass");
var util = require("gulp-util");
var sourcemaps = require("gulp-sourcemaps");


var cssSrc = "./src/css/**/*.scss";
var jsSrc = "./src/js/*.js";
var imagesSrc = "./src/images/*.*";
var htmlSrc = "./templates/**/*.html";
var cssDist = "./dist/css/";
var jsDist = "./dist/js/";
var imagesDist = "./dist/images";


gulp.task("html", function () {
	gulp.src(htmlSrc)
		.pipe(bs.stream())
});


gulp.task("css", function(){
	gulp.src(cssSrc)
		.pipe(sass().on("error", sass.logError))
		.pipe(cssnano())
		.pipe(rename({"suffix": ".min"}))
		.pipe(gulp.dest(cssDist))
		.pipe(bs.stream())
});

gulp.task("js", function(){
	gulp.src(jsSrc)
		.pipe(sourcemaps.init())
		.pipe(uglify().on("error", util.log))
		.pipe(rename({"suffix": ".min"}))
		.pipe(sourcemaps.write())
		.pipe(gulp.dest(jsDist))
		.pipe(bs.stream())
});

gulp.task("images", function(){
	gulp.src(imagesSrc)
		.pipe(cache(imagemin()))
		.pipe(gulp.dest(imagesDist))
		.pipe(bs.stream())
});

gulp.task("watch", function(){
	gulp.watch(cssSrc, ["css"]);
	gulp.watch(jsSrc, ["js"]);
	gulp.watch(imagesSrc, ["images"]);
	gulp.watch(htmlSrc, ["html"]);
});

gulp.task("bs", function(){
	bs.init({
		"server": {
			"baseDir": "./"
		}
	})
});

// gulp.task("default", ["bs", "watch", "html"]);
gulp.task("default", ["watch"]);