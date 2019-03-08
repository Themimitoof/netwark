const gulp = require('gulp'),
    watch = require('gulp-watch'),
    sass = require('gulp-sass'),
    rename = require('gulp-rename'),
    uglify = require('gulp-uglify'),
    sourcemaps = require('gulp-sourcemaps');


/**
 * CSS Tasks
 */
gulp.task('css', () => {
    return gulp.src('./assets/scss/main.scss')
        .pipe(sass({
            outputStyle: 'compressed'
        }).on('error', sass.logError))
        .pipe(rename('app.css'))
        .pipe(gulp.dest('./dist/css'))
});
