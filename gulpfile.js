const gulp = require('gulp'),
    sass = require('gulp-sass'),
    rename = require('gulp-rename'),
    minify = require('gulp-minify'),
    concat = require('gulp-concat');

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


gulp.task('css:watch', () => {
    return gulp.watch('./assets/scss/**', gulp.series('css'));
});

/**
 * JS Tasks
 */
gulp.task('js', () => {
    return gulp.src(['./assets/js/*.js'])
        .pipe(concat('app.js'))
        .pipe(minify())
        .pipe(gulp.dest('./dist/js/'));
});

gulp.task('js:watch', () => {
    return gulp.watch('./assets/js/**', gulp.series('js'));
});


/**
 * General and default tasks
 */

gulp.task('all', gulp.series('css', 'js'));
gulp.task('all:watch', gulp.parallel('css:watch', 'js:watch'));
gulp.task('default', gulp.series('all'));