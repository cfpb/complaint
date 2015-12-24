'use strict';

var gulp = require( 'gulp' );
var $ = require( 'gulp-load-plugins' )();
var config = require( '../config' ).test;
var handleErrors = require( '../utils/handleErrors' );

gulp.task( 'test:unit', function( cb ) {
  gulp.src( config.src )
    .pipe( $.istanbul( {
      includeUntested: true
    } ) )
    .pipe( $.istanbul.hookRequire() )
    .on( 'finish', function() {
      gulp.src( config.tests + '/unit_tests/*.js' )
        .pipe( $.mocha( {
          reporter: 'nyan', 
          timeout: 20000
        } ) )
        .pipe( $.istanbul.writeReports( {
          dir: config.tests + '/unit_test_coverage'
        } ) )

        /* TODO: we want this but it breaks because we don't have good coverage
        .pipe( $.istanbul.enforceThresholds( {
          thresholds: { global: 90 }
        } ) )
        */

        .on( 'end', cb );
    } );
} );

gulp.task( 'test',
  [
    'test:unit',
  ]
);
