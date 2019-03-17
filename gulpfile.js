const gulp = require('gulp'),
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


gulp.task('css:watch', () => {
    return gulp.watch('./assets/scss/main.scss', ['css']);
 });
