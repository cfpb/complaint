'use strict';

var fs = require( 'fs' );

/**
 * Set up file paths
 */
var loc = {
  src:  './src',
  dist: './complaint_common/static/complaint_common/',
  lib:  JSON.parse( fs.readFileSync( './.bowerrc' ) ).directory, // eslint-disable-line no-sync, no-inline-comments, max-len
  test: './test',
  templ: './complaint_common/templates/standalone/'
};

module.exports = {
  pkg:    JSON.parse( fs.readFileSync( 'bower.json' ) ), // eslint-disable-line no-sync, no-inline-comments, max-len
  banner:
      '/*!\n' +
      ' *  <%= pkg.name %> - v<%= pkg.version %>\n' +
      ' *  <%= pkg.homepage %>\n' +
      ' *  Licensed <%= pkg.license %> by Consumer Financial Protection Bureau christopher.contolini@cfpb.gov\n' +
      ' */',
  lint: {
    src: [
      loc.src + '/static/js/**/*.js',
      loc.test + '/unit_tests/**/*.js',
      loc.test + '/browser_tests/**/*.js'
    ],
    gulp: [
      'gulpfile.js',
      'gulp/**/*.js'
    ]
  },
  clean: {
    dest: loc.dist,
    templ: loc.templ
  },
  styles: {
    cwd:      loc.src + '/static/css',
    src:      '/main.less',
    dest:     loc.dist + '/css',
    settings: {
      paths: [
        loc.lib,
        loc.lib + '/cf-typography/src'
      ],
      compress: true
    }
  },
  scripts: {
    entries: ['index.js', 'data-use.js', 'submit-a-complaint.js', 'complaint-process.js'],
    src: loc.src + '/static/js/',
    dest: loc.dist + '/js/',
    common: 'main.js',
    ie8: [loc.lib + '/respond/src/respond.js', loc.lib + '/ie8/build/ie8.js']
  },
  test: {
    src: [loc.src + '/static/js/index.js', loc.src + '/static/js/data-use.js', loc.src + '/static/js/handle-resize.js', loc.src + '/static/js/expandable-helpers.js', loc.src + '/static/js/tab-expandables.js'],
    tests: loc.test
  },
  browserify: {
    paths: {
      scripts: 'src/js/index.js',
      dest: 'dist/scripts/'
    }
  },
  images: {
    src:  loc.src + '/static/img/**',
    dest: loc.dist + '/img'
  },
  copy: {
    files: {
      src: [
        loc.src + '/**/*.html',
        loc.src + '/**/*.pdf',
        loc.src + '/_*/**/*',
        loc.src + '/robots.txt',
        loc.src + '/favicon.ico',
        '!' + loc.lib + '/**/*.html'
      ],
      dest: loc.dist
    },
    css: {
      src:  loc.src + '/static/css/index.css',
      dest: loc.dist + '/css/'
    },
    icons: {
      src:  loc.lib + '/cf-icons/src/fonts/*',
      dest: loc.dist + '/fonts/'
    },
    vendorjs: {
      src: [
        loc.lib + '/box-sizing-polyfill/boxsizing.htc',
        loc.lib + '/html5shiv/dist/html5shiv-printshiv.min.js'
      ],
      dest: loc.dist + '/js/'
    },
    templates: {
      src:  loc.lib + '/django-assets/templates/*.html',
      dest: loc.templ
    },
    nemoless: {
      src:  loc.lib + '/django-assets/static/css/*.less',
      dest: loc.src + '/static/css/'
    },
    nemojs: {
      src:  loc.lib + '/django-assets/static/js/*.js',
      dest: loc.src + '/static/js/'
    }
  }
};
