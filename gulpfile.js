const fs = require('fs'),
    gulp = require('gulp'),
    sass = require('gulp-sass'),
    rename = require('gulp-rename'),
    terser = require('gulp-terser'),
    replace = require('gulp-replace'),
    browserify = require('browserify'),
    buffer = require('vinyl-buffer'),
    source = require('vinyl-source-stream');

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
    // Get Mapbox access token
    var token = fs.readFileSync(__dirname + '/.mapbox-token', 'utf-8', 'r').toString().replace('\n', '');
    var b = browserify({
        entries: './assets/js/app.js',
    });

    // Task process
    return b.bundle()
        .pipe(source('app.js'))
        .pipe(replace('replaced-mapbox-access-token', token))
        .pipe(buffer())
        .pipe(terser())
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